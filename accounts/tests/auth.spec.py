from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from accounts.models import User


class TestAuth(APITestCase):

    def test_register_user_success(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])

    def test_login_user_success(self):
        url = reverse('login')
        user = User.objects.create_user(
            email='john.doe@example.com',
            firstName='John',
            lastName='Doe',
            password='password123'
        )
        data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])
