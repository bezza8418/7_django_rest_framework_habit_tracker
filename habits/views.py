from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Habit
from .serializers import HabitSerializer
from .paginators import HabitPagination


@extend_schema_view(
    list=extend_schema(summary='Список своих привычек', description='Возвращает привычки текущего пользователя с пагинацией.'),
    create=extend_schema(summary='Создание привычки', description='Создаёт новую привычку для текущего пользователя.'),
    retrieve=extend_schema(summary='Получение привычки', description='Возвращает одну привычку по ID.'),
    update=extend_schema(summary='Обновление привычки', description='Полное обновление привычки.'),
    partial_update=extend_schema(summary='Частичное обновление', description='Частичное обновление привычки.'),
    destroy=extend_schema(summary='Удаление привычки', description='Удаляет привычку.'),
)
class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек пользователя"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(summary='Список публичных привычек', description='Возвращает публичные привычки всех пользователей.'),
    retrieve=extend_schema(summary='Получение публичной привычки', description='Возвращает одну публичную привычку по ID.'),
)
class PublicHabitListView(viewsets.ReadOnlyModelViewSet):
    """Список публичных привычек (только просмотр)"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
