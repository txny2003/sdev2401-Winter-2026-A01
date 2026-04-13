from rest_framework import serializers

from .models import Exercise, Workout, WorkoutLog

# beacuse settings.authusermodel... is a string
# we're going to have import the User class
# either our custom one or the one from django
from django.contrib.auth.models import User


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["id", "title", "date"]


class ExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    exercise_type = serializers.ChoiceField(choices=Exercise.EXERCISE_TYPES)

    def validate_name(self, value):
        INVALID_EXERCISE_NAMES = ["sitting", "lying down"]
        if value in INVALID_EXERCISE_NAMES:
            raise serializers.ValidationError(
                "Exercise name cannot be 'sitting' or 'lying down'."
            )
        return value

    # these methods are called by the save method.
    def create(self, validated_data):
        return Exercise.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.exercise_type = validated_data.get(
            "exercise_type", instance.exercise_type
        )
        instance.save()
        return instance


class UserReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
        ]


class WorkoutLogReadOnlySerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer(read_only=True)
    exercise = ExerciseSerializer(read_only=True)
    user = UserReadOnlySerializer(read_only=True)

    # I want you to create the meta
    # I want you to serialize the exercise and workout using
    # the existing serializers.
    class Meta:
        model = WorkoutLog
        fields = [
            "id",
            "user",
            # foreign keys that we're going to override
            "workout",
            "exercise",
            # plain old fields
            "sets",
            "reps",
            "weight_kg",
            "time",
        ]


class WorkLogCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutLog
        fields = [
            "id",
            # foreign keys that we're going to override
            "user",
            "workout",  # this will only be the id
            "exercise",  # this will only be the id
            # plain old fields
            "sets",
            "reps",
            "weight_kg",
            "time",
        ]

    # note: the save, create, update methods
    # are created automatically because it's part
    # of the ModelSerializer class.

    # validation
    # we're going to validate that cardio workouts
    # can't have a wieght kg.
    def validate(self, data):
        exercise = data.get("exercise")  # this will be a db instance
        # deal with if it's a patch/post
        # there shoudl be an instance.
        if exercise is None and self.instance is not None:
            exercise = self.instance.exercise
        weight_kg = data.get("weight_kg")

        # I want to skip this validation if it's a partial
        if exercise is None or weight_kg is None:
            # successful validation
            return data

        # say if they exercise type is cardio we can't have a weight kg.
        if exercise.exercise_type == "cardio" and weight_kg is not None:
            raise serializers.ValidationError(
                "Cardio workouts can't have weights",
            )

        # default successful return
        return data

    # validate the weight_kg field
    # we can't have negative weights
    # we can't have weight 500kgs
    def validate_weight_kg(self, value):
        # do it
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Weight can't be negative.",
            )
        if value is not None and value > 500:
            raise serializers.ValidationError(
                "Come on. Weight can't be greater than 500"
            )

        # default the success
        return value
