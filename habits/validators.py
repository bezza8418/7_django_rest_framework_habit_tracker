from rest_framework import serializers


def validate_reward_and_linked_habit(value):
    """
    Исключает одновременный выбор связанной привычки и указания вознаграждения.
    """
    reward = value.get('reward')
    linked_habit = value.get('linked_habit')

    if reward and linked_habit:
        raise serializers.ValidationError(
            'Нельзя одновременно указывать вознаграждение и связанную привычку.'
        )


def validate_duration(value):
    """
    Время выполнения должно быть не больше 120 секунд.
    """
    if value > 120:
        raise serializers.ValidationError(
            'Время выполнения не должно превышать 120 секунд.'
        )


def validate_linked_habit_is_pleasant(value):
    """
    В связанные привычки могут попадать только привычки с признаком приятной привычки.
    """
    linked_habit = value.get('linked_habit')

    if linked_habit and not linked_habit.is_pleasant:
        raise serializers.ValidationError(
            'Связанная привычка должна быть приятной.'
        )


def validate_pleasant_habit(value):
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """
    is_pleasant = value.get('is_pleasant')
    reward = value.get('reward')
    linked_habit = value.get('linked_habit')

    if is_pleasant and (reward or linked_habit):
        raise serializers.ValidationError(
            'У приятной привычки не может быть вознаграждения или связанной привычки.'
        )


def validate_periodicity(value):
    """
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    """
    if value < 1 or value > 7:
        raise serializers.ValidationError(
            'Периодичность должна быть от 1 до 7 дней.'
        )
    