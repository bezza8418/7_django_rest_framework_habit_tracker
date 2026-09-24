from rest_framework import serializers
from .models import Habit
from .validators import (
    validate_reward_and_linked_habit,
    validate_duration,
    validate_linked_habit_is_pleasant,
    validate_pleasant_habit,
    validate_periodicity,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            validate_reward_and_linked_habit,
            validate_linked_habit_is_pleasant,
            validate_pleasant_habit,
        ]

    def validate_duration(self, value):
        validate_duration(value)
        return value

    def validate_periodicity(self, value):
        validate_periodicity(value)
        return value
