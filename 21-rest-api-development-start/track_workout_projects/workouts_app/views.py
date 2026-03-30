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
    def get(self, request):
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
