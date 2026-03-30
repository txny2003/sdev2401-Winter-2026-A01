from django.db import models


# Create your models here.
class Exercise(models.Model):
    # we're looking at the
    # tuples for the items.
    # left is the value
    # right is what is display as an option in the
    # admin.
    EXERCISE_TYPES = [
        ("cardio", "Cardio"),
        ("strength", "Strength"),
        ("flexibility", "Flexibility"),
        ("balance", "Balance"),
    ]
    # Note you can make these same.

    name = models.CharField(max_length=100)
    exercise_type = models.CharField(
        max_length=50,
        choices=EXERCISE_TYPES,
    )

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

    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="logs")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(blank=True, null=True)
    reps = models.IntegerField(blank=True, null=True)
    weight_kg = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"{self.workout.title} - {self.exercise.name}"
