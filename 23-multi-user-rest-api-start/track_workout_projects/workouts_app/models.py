from django.db import models

# use the settings.AUTH_USER_MODEL to import the user.
from django.conf import settings


# Create your models here.
class Exercise(models.Model):
    EXERCISE_TYPES = [
        ("cardio", "Cardio"),
        ("strength", "Strength"),
        ("flexibility", "Flexibility"),
        ("balance", "Balance"),
    ]

    name = models.CharField(max_length=100)
    exercise_type = models.CharField(max_length=50, choices=EXERCISE_TYPES)

    def __str__(self):
        return f"{self.name} ({self.exercise_type})"


class Workout(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    # Linking many exercises to many workouts

    def __str__(self):
        return f"{self.title}"


class WorkoutLog(models.Model):
    """Tracking specific performance for an exercise in a workout"""

    # add the user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # foreign key items
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="logs")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    # normal database pieces.
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    weight_kg = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"{self.workout.title} - {self.exercise.name}"
