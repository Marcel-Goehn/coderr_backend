from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTests(APITestCase):
    
    def test_registration_successful(self):
        url = reverse("registration")
        data = {
            "username": "testuser",
            "email": "testmail@gmail.com",
            "password": "testpassword123",
            "repeated_password": "testpassword123",
            "type": "business"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("user_id", response.data)
        
    def test_registration_username_is_missing(self):
        url = reverse("registration")
        data = {
            "email": "testmail@gmail.com",
            "password": "testpassword123",
            "repeated_password": "testpassword123",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_email_is_missing(self):
        url = reverse("registration")
        data = {
            "username": "testuser",
            "password": "testpassword123",
            "repeated_password": "testpassword123",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_password_is_missing(self):
        url = reverse("registration")
        data = {
            "username": "testuser",
            "email": "testmail@gmail.com",
            "repeated_password": "testpassword123",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_repeated_password_is_missing(self):
        url = reverse("registration")
        data = {
            "username": "testuser",
            "email": "testmail@gmail.com",
            "password": "testpassword123",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_type_is_missing(self):
        url = reverse("registration")
        data = {
            "username": "testuser",
            "email": "testmail@gmail.com",
            "password": "testpassword123",
            "repeated_password": "testpassword123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_passwords_dont_match(self):
        url = reverse("registration")
        data = {
            "username": "testuser",
            "email": "testmail@gmail.com",
            "password": "testpassword123",
            "repeated_password": "testpassword1234",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_type_is_not_customer_or_business(self):
        url = reverse("registration")
        data = {
            "username": "testuser",
            "email": "testmail@gmail.com",
            "password": "testpassword123",
            "repeated_password": "testpassword123",
            "type": "apple"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_username_is_already_in_use(self):
        User.objects.create_user(username="Marcel", password="MarcelTestPassword123")
        url = reverse("registration")
        data = {
            "username": "Marcel",
            "email": "testmail@gmail.com",
            "password": "testpassword123",
            "repeated_password": "testpassword123",
            "type": "business"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_email_is_already_in_use(self):
        User.objects.create_user(username="Marcel", password="MarcelTestPassword123", email="testmail@test.com")
        url = reverse("registration")
        data = {
            "username": "Marcel",
            "email": "testmail@test.com",
            "password": "testpassword123",
            "repeated_password": "testpassword123",
            "type": "business"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)