from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import Group
from users.models import User
from habits.models import Habit


class HabitModelTestCase(TestCase):
    """Тесты модели Habit"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='habit_user@example.com',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='20:00',
            action='Принять ванну',
            is_pleasant=True,
            duration=60,
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='07:00',
            action='Прогулка',
            duration=120,
            linked_habit=self.pleasant_habit,
        )

    def test_habit_creation(self):
        """Привычка создаётся корректно"""
        self.assertEqual(self.habit.action, 'Прогулка')
        self.assertEqual(self.habit.user, self.user)
        self.assertEqual(self.habit.linked_habit, self.pleasant_habit)

    def test_habit_str(self):
        """Метод __str__ возвращает корректную строку"""
        self.assertIn('Прогулка', str(self.habit))
        self.assertIn(self.user.email, str(self.habit))


class HabitValidatorTestCase(TestCase):
    """Тесты валидаторов Habit"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='validator_user@example.com',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='20:00',
            action='Ванна',
            is_pleasant=True,
            duration=60,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_reward_and_linked_habit_conflict(self):
        """Нельзя одновременно reward и linked_habit"""
        data = {
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'duration': 60,
            'reward': 'Кофе',
            'linked_habit': self.pleasant_habit.id,
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duration_limit(self):
        """Время выполнения не больше 120 секунд"""
        data = {
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'duration': 200,
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_habit_cannot_have_reward(self):
        """У приятной привычки не может быть вознаграждения"""
        data = {
            'place': 'Дом',
            'time': '20:00',
            'action': 'Ванна',
            'is_pleasant': True,
            'duration': 60,
            'reward': 'Шоколад',
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_linked_habit_must_be_pleasant(self):
        """Связанная привычка должна быть приятной"""
        useful_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='06:00',
            action='Полезная привычка',
            duration=60,
        )
        data = {
            'place': 'Парк',
            'time': '07:00',
            'action': 'Прогулка',
            'duration': 60,
            'linked_habit': useful_habit.id,
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_limit(self):
        """Периодичность не больше 7 дней"""
        data = {
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'duration': 60,
            'periodicity': 10,
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HabitAPITestCase(TestCase):
    """Тесты CRUD для привычек"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='api_user@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            email='api_other@example.com',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='07:00',
            action='Прогулка',
            duration=120,
        )
        self.public_habit = Habit.objects.create(
            user=self.other_user,
            place='Спортзал',
            time='18:00',
            action='Тренировка',
            duration=60,
            is_public=True,
        )
        self.client = APIClient()

    def test_habit_list_unauthorized(self):
        """Неавторизованный не видит список"""
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_list_authenticated(self):
        """Авторизованный видит свои привычки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_habit_create(self):
        """Создание привычки"""
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'Дом',
            'time': '08:00',
            'action': 'Зарядка',
            'duration': 60,
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)

    def test_habit_update_own(self):
        """Обновление своей привычки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/habits/{self.habit.id}/', {'action': 'Новая прогулка'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update_other(self):
        """Нельзя обновить чужую привычку"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(f'/api/habits/{self.habit.id}/', {'action': 'Взлом'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_habit_delete_own(self):
        """Удаление своей привычки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_public_habits_list(self):
        """Список публичных привычек"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/public-habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_pagination(self):
        """Пагинация по 5 привычек"""
        self.client.force_authenticate(user=self.user)
        for i in range(7):
            Habit.objects.create(
                user=self.user,
                place=f'Место {i}',
                time='10:00',
                action=f'Действие {i}',
                duration=60,
            )
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
