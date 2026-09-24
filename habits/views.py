from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from .paginators import HabitPagination


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек пользователя"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Пользователь видит только свои привычки"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Привязываем привычку к текущему пользователю"""
        serializer.save(user=self.request.user)


class PublicHabitListView(viewsets.ReadOnlyModelViewSet):
    """Список публичных привычек (только просмотр)"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Только публичные привычки"""
        return Habit.objects.filter(is_public=True)
