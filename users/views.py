from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя (доступна без авторизации)"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary='Регистрация пользователя',
        description='Создаёт нового пользователя. Доступно без авторизации.',
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
