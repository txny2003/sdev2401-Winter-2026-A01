from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import (
    ExerciseSerializer,
    WorkoutSerializer,
    WorkLogCreateUpdateSerializer,
    WorkoutLogReadOnlySerializer,
)
from .models import Exercise, Workout, WorkoutLog


class WorkoutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class ExerciseAPIView(APIView):
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
    # authenticated users only
    permission_classes = [IsAuthenticated]

    # we can override the default value of a
    # serializer class with a method named
    # get_serializer_class
    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return WorkLogCreateUpdateSerializer
        # for get and other methods
        return WorkoutLogReadOnlySerializer

    # we are overriding the queryset vlaue
    # with a get_querset method
    def get_queryset(self):
        return WorkoutLog.object.all()

    def get(self, request, id=None):
        # detail view
        if id:
            workout_log = get_object_or_404(WorkoutLog, id=id)
            # remember folks this is the same as
            # workout_log = WorkoutLog.objects.get(id=id) with a 404
            serializer = self.get_serializer_class()(workout_log)
            # self.get_serializer_class() returns a ref to the
            # the serializer class.
            # above we are initializing the class with our model instance
            return Response(serializer.data)
        # list view
        # let's get themfrom the db.
        workout_logs = self.get_queryset()
        # we're going to use our get_serializer
        # self.get_serializer_class() returns
        # WorkoutLogReadOnlySerializer
        serializer = self.get_serializer_class()(
            workout_logs,
            many=True,  # queryset (many items from the db)
        )
        return Response(serializer.data)
