from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """Модель привычки"""

    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Раз в 2 дня'),
        (3, 'Раз в 3 дня'),
        (4, 'Раз в 4 дня'),
        (5, 'Раз в 5 дней'),
        (6, 'Раз в 6 дней'),
        (7, 'Раз в 7 дней'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место'
    )
    time = models.TimeField(
        verbose_name='Время'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Связанная привычка',
        **NULLABLE
    )
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        verbose_name='Периодичность (в днях)'
    )
    reward = models.CharField(
        max_length=255,
        verbose_name='Вознаграждение',
        **NULLABLE
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name='Время на выполнение (секунды)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['id']

    def __str__(self):
        return f'{self.user.email} - {self.action}'
