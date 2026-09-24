from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User


class UserRegistrationTestCase(TestCase):
    """Тесты регистрации пользователей"""

    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        """Успешная регистрация"""
        data = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_register_duplicate_email(self):
        """Регистрация с существующим email"""
        User.objects.create_user(email='existing@example.com', password='testpass123')
        data = {
            'email': 'existing@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        """Несовпадение паролей"""
        data = {
            'email': 'newuser2@example.com',
            'password': 'testpass123',
            'password_confirm': 'different',
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
