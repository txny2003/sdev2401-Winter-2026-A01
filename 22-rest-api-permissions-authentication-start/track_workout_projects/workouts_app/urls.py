from .views import ExerciseAPIView, WorkoutViewSet

# import router from rest framework
from rest_framework.routers import DefaultRouter

from django.urls import path

# Create a default router and add our viewset.
router = DefaultRouter()
# let's register all the endpoints for our viewset
router.register(r"workouts", WorkoutViewSet)

urlpatterns = [
    # the two paths for the apiviews.
    path("exercises/", ExerciseAPIView.as_view(), name="exercise-api"),
    path("exercises/<int:id>/", ExerciseAPIView.as_view(), name="exercise-detail"),
] + router.urls  # going to add all of the paths.
