from django.shortcuts import get_object_or_404

# import the APIView which will
# behave a lot like a class based view.
from rest_framework.views import APIView

# response is like render except it just
# gives the JSON.
from rest_framework.response import Response

# we need our model and our serializer here
from .serializers import ExerciseSerializer
from .models import Exercise


# create our apiview class.
class ExerciseAPIView(APIView):

    # get from the database.
    def get_queryset(self):
        return Exercise.objects.all()

    # create the get just like we did in the past.
    # extend this to allow the detail get as well.
    def get(self, request, id=None):
        # a detail view
        if id is not None:
            # get from db.
            exercise = get_object_or_404(Exercise, id=id)
            # serialize the single instance
            serializer = ExerciseSerializer(exercise)
            # note not many is true because it's a single instance
            # return early.
            return Response(serializer.data)

        # list view
        # APIView expect a function called
        # get_queryset, how to fetch from the DB.
        exercises = self.get_queryset()
        # we're going serialize this data
        # note they will be many!
        serializer = ExerciseSerializer(
            exercises,
            many=True,
        )
        # return a response
        return Response(serializer.data)

    # Build the delete endpoint.
    # needs a specific id
    def delete(self, request, id):
        exercise = get_object_or_404(Exercise, id=id)

        # delete
        exercise.delete()
        # note: you could make this a flag and then change your serializer
        # to hide this flag and also filter this in the get queryset.
        return Response(status=204)

    # two requests to handle:put and patch note they need the id of the item that
    # they want to change.
    # we're goign to make a single function that will handle both.
    def update(self, request, id, partial=False):
        # retrieve the object
        exercise = get_object_or_404(Exercise, id=id)
        # create serializer (we're going to pass an instance.)
        serializer = ExerciseSerializer(
            exercise,  # instance
            data=request.data,  # data from user
            partial=partial,  # False for put, true for patch
        )
        # validate it.
        if serializer.is_valid():
            # save it (on the serializer.)
            updated_exercise = serializer.save()  # returns a model instance
            # serialize and show the data
            # give a response if success
            return Response(ExerciseSerializer(updated_exercise).data)
        # give a response if error
        return Response(serializer.errors, status=400)

    # put (full update)
    def put(self, request, id):
        # a full update
        return self.update(request, id, partial=False)

    # patch (partial update)
    def patch(self, request, id):
        # only modifies a part.
        return self.update(request, id, partial=True)

    # create a post request.
    def post(self, request):

        # we want the deserialization step
        serializer = ExerciseSerializer(data=request.data)

        # just like forms we're going to check if the
        # serializer is valid
        if serializer.is_valid():
            # we're going to save and get the instance
            exercise = serializer.save()

            # return a successful response
            return Response(
                ExerciseSerializer(exercise).data, status=201  # created status.
            )
        # handle the errors
        # return a response with errors outside of the is valid
        return Response(
            serializer.errors,
            status=400,  # bad request
        )
