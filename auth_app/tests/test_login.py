from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword123", email="testmail@test.com")
        self.token = Token.objects.create(user=self.user)
    
    def test_successful_login(self):
        url = reverse("login")
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("user_id", response.data)
    
    def test_username_is_missing(self):
        url = reverse("login")
        data = {
            "password": "testpassword123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_is_missing(self):
        url = reverse("login")
        data = {
            "username": "testuser"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_is_not_matching(self):
        url = reverse("login")
        data = {
            "username": "testuser",
            "password": "testpassword1234"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)