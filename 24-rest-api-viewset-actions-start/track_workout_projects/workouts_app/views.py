from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# let's import this action which will allow us to extend the viewset.
from rest_framework.decorators import action

# we're going to import the search filter
from rest_framework import filters

from .permissions import IsOwnerOfResourceOrReadOnly
from .serializers import (
    ExerciseSerializer,
    WorkoutSerializer,
    WorkoutDetailReadOnlySerializer,  # import the serializer
    WorkoutLogReadOnlySerializer,
    WorkoutLogCreateUpdateSerializer,
)

from .models import Exercise, Workout, WorkoutLog


class WorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    # search filter
    filter_backends = [filters.SearchFilter]
    # this above is going to make it so that I can add
    # the search query parameters
    search_fields = ["title"]
    # this is going to search on the title field
    # again this is basic for more information take a
    # look at opensearch, elasticsearch, apache solr
    # it's a big thing.

    # we're going to create an action.
    # where we get the workoutlogs and the workouts
    # for a given workout
    @action(
        detail=True,  # means you need the id (or pk.)
        methods=["GET"],  # the request methods allowed
        url_path="detail",  # the trailing part of the path.
    )
    def workout_logs(
        self, request, pk=None
    ):  # the default for a detail action (a non detail action has no pk.)
        # get the object
        workout = self.get_object()  # the detailed instance.

        # create a serializer for our workout and its' logs.
        serializer = WorkoutDetailReadOnlySerializer(workout)

        # return that response.
        return Response(serializer.data)


class ExerciseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        # detail view
        if id:
            exercise = get_object_or_404(Exercise, id=id)
            serializer = ExerciseSerializer(exercise)
            return Response(serializer.data)
        # list view
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            exercise = serializer.save()
            # this will call the create method internally.
            return Response(ExerciseSerializer(exercise).data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, id, partial=False):
        exercise = get_object_or_404(Exercise, id=id)
        serializer = ExerciseSerializer(exercise, data=request.data, partial=partial)
        if serializer.is_valid():
            exercise = serializer.save()
            return Response(ExerciseSerializer(exercise).data)
        return Response(serializer.errors, status=400)

    # we can use the same update function for both PUT and PATCH requests by passing in the partial argument
    def put(self, request, id):
        return self.update(request, id, partial=False)

    def patch(self, request, id):
        return self.update(request, id, partial=True)

    def delete(self, request, id):
        exercise = get_object_or_404(Exercise, id=id)
        exercise.delete()
        return Response(status=204)


class WorkoutLogAPIView(APIView):
    permission_classes = [IsOwnerOfResourceOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return WorkoutLogCreateUpdateSerializer
        return WorkoutLogReadOnlySerializer

    def get(self, request, id=None):
        # detail view
        if id:
            workout_log = get_object_or_404(WorkoutLog, id=id)
            serializer = self.get_serializer_class()(workout_log)
            return Response(serializer.data)
        # list view
        workout_logs = WorkoutLog.objects.all()
        serializer = self.get_serializer_class()(workout_logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        # get the serializer class based on the request method
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            workout_log = serializer.save(user=request.user)
            # return the workout log with the read only serializer to include the workout and exercise information in the response
            return Response(WorkoutLogReadOnlySerializer(workout_log).data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, id, partial=False):
        workout_log = get_object_or_404(WorkoutLog, id=id)
        # This triggers the 'has_object_permission' method in IsOwner
        self.check_object_permissions(request, workout_log)

        serializer = self.get_serializer_class()(
            workout_log, data=request.data, partial=partial
        )
        if serializer.is_valid():
            workout_log = serializer.save(user=request.user)
            return Response(WorkoutLogReadOnlySerializer(workout_log).data)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        return self.update(request, id, partial=False)

    def patch(self, request, id):
        return self.update(request, id, partial=True)
