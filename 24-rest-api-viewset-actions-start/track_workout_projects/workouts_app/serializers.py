from rest_framework import serializers

from .models import Exercise, Workout, WorkoutLog
from django.conf import settings
from django.contrib.auth.models import User

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'title', 'date']

class ExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    exercise_type = serializers.ChoiceField(choices=Exercise.EXERCISE_TYPES)

    def validate_name(self, value):
        INVALID_EXERCISE_NAMES = ["sitting", "lying down"]
        if value in INVALID_EXERCISE_NAMES:
            raise serializers.ValidationError("Exercise name cannot be 'sitting' or 'lying down'.")
        return value

    def create(self, validated_data):
        return Exercise.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.exercise_type = validated_data.get('exercise_type', instance.exercise_type)
        instance.save()
        return instance

# user serializer to only include public information.
class UserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Read only serializer for viewing workouts that includes the user field
class WorkoutLogReadOnlySerializer(serializers.ModelSerializer):
    # include the workout's information in the response
    workout = WorkoutSerializer(read_only=True)
    # include the exercises in the workout log
    exercise = ExerciseSerializer(read_only=True)
    # include the user's information in the response
    user = UserReadOnlySerializer(read_only=True)

    class Meta:
        model = WorkoutLog
        fields = [
            'id',
            'sets',
            'reps',
            'weight_kg',
            'time',
            # override the default
            'workout',
            'exercise',
            # include the user field in the read only serializer
            'user'
        ]
        # if you add the depth option to the serializer's Meta class,
        # it will automatically include the related data for foreign key fields in the response. In this case, it will include the user's information in the response when viewing workouts.
        depth = 1

# Serializer for creating/updating workouts that doesn't include the user field
class WorkoutLogCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = [
            'id',
            'sets',
            'reps',
            'weight_kg',
            'time',
            # foreign key fields
            'workout',
            'exercise',
            # include the user field.
            'user'
        ]

    def validate_weight_kg(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Weight cannot be negative.")
        elif value is not None and value > 500:
            raise serializers.ValidationError("Weight cannot be greater than 500 kg.")
        return value

    # let's validate that weight_kg is not set for cardio exercises
    def validate(self, data):
        # this will be an exercise instance because we're using a ModelSerializer and the exercise field is a foreign key to the Exercise model


        exercise = data.get('exercise')
        weight_kg = data.get('weight_kg')

        # skip this if a partial update (used for patch)
        if exercise is None or weight_kg is None:
            return data

        # we need to get the exercise from the database to check if it's a cardio exercise
        if exercise.exercise_type == "cardio" and weight_kg is not None:
            raise serializers.ValidationError("Cardio exercises cannot have a weight.")
        return data
