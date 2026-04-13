from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOfResourceOrReadOnly

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
    def get_queryset(self):
        return Exercise.objects.all()

    def get(self, request, id=None):
        # detail view
        if id:
            exercise = get_object_or_404(Exercise, id=id)
            serializer = ExerciseSerializer(exercise)
            return Response(serializer.data)
        # list view
        exercises = self.get_queryset()
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
    # only owners of the workout log will be able to update their own items.
    permission_classes = [IsAuthenticated | IsOwnerOfResourceOrReadOnly]

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
        # i'm going to return only items for the given
        # user.
        return WorkoutLog.objects.filter(user=self.request.user)

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

    # for a post I want you folks to use the get serializer class to deserialize the data
    # but I want you use the readonly serializer on response.
    def post(self, request):
        # just like we have in the past we're going to get the serializer class
        # and check if it's valid.
        serializer = self.get_serializer_class()(
            data=request.data  # raw data from the request
        )
        if serializer.is_valid():  # cleaning a validation
            # create a work out log instance
            workout_log = serializer.save(
                # from the token that is authenticating
                # the user.
                user=self.request.user
            )

            # we're going to use this instance in a read only serializer
            # returns more detailed data than what you sent.
            return Response(
                WorkoutLogReadOnlySerializer(
                    workout_log
                ).data,  # our detailed representation
                status=201,  # status for created
            )

        return Response(
            serializer.errors,  # defined on the is_valid method
            status=400,  # bad request.
        )

    def update(self, request, id, partial=False):
        # we need to get item from the db.
        workout_log = get_object_or_404(WorkoutLog, id=id)
        # we need to explicitly call the object permission in an api view.
        self.check_object_permissions(request, workout_log)
        # we need to use the serializer on ingesting.
        serializer = self.get_serializer_class()(
            workout_log,  # pass the instance
            data=request.data,  # what the user is trying to change
            partial=True,  # handle each.
        )
        if serializer.is_valid():  # clean sanitization.
            # we need to save it to the db.
            update_workout_log = serializer.save(
                # from the token that is authenticating
                # the user.
                user=self.request.user
            )
            # this is where the interesting jazz goes.
            return Response(
                WorkoutLogReadOnlySerializer(update_workout_log).data,
                status=200,
            )
        return Response(
            serializer.errors,
            status=400,
        )

    # create the patch
    def patch(self, request, id):
        return self.update(request, id, partial=True)

    # and put methods that use the update
    def put(self, request, id):
        return self.update(request, id, partial=False)
