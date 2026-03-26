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

    def get_queryset(self):
        return Exercise.objects.all()

    # create the get just like we did in the past.
    def get(self, request):
        # APIView expect a function called
        # get_queryset, how to fetch from the DB.

