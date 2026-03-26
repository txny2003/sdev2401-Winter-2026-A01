# import django urls path
from django.urls import path

from .views import ExerciseAPIView

urlpatterns = [
    path(
        "exercises/",
        ExerciseAPIView.as_view(),
        name="exercise-api",
    )
]
