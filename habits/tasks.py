from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_habit_reminder(habit_id):
    """
    Отправляет напоминание о привычке в Telegram.

    :param habit_id: ID привычки
    """
    from habits.models import Habit
    from telegram_bot.services import send_telegram_message

    try:
        habit = Habit.objects.select_related('user').get(id=habit_id)
    except Habit.DoesNotExist:
        return f'Привычка с id={habit_id} не найдена'

    if not habit.user.telegram_chat_id:
        return f'У пользователя {habit.user.email} не указан telegram_chat_id'

    text = (
        f'⏰ Напоминание!\n\n'
        f'Действие: {habit.action}\n'
        f'Место: {habit.place}\n'
        f'Время: {habit.time.strftime("%H:%M")}\n'
        f'Длительность: {habit.duration} сек.'
    )

    send_telegram_message(habit.user.telegram_chat_id, text)
    return f'Напоминание отправлено для привычки "{habit.action}"'


@shared_task
def check_habits_for_reminders():
    """
    Проверяет все привычки и отправляет напоминания тем,
    у которых время выполнения совпадает с текущим.
    """
    from habits.models import Habit

    now = timezone.localtime()
    current_time = now.time()

    # Находим привычки, время которых наступило (в пределах минуты)
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
    ).select_related('user')

    count = 0
    for habit in habits:
        if habit.user.telegram_chat_id:
            send_habit_reminder.delay(habit.id)
            count += 1

    return f'Отправлено напоминаний: {count}'
