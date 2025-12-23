from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from auth_app.models import UserProfile
from auth_app.api.serializers import ProfileSerializer


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword123", email="testmail@mail.com")
        self.profile = UserProfile.objects.create(user=self.user, type="business")
    
    def test_successfully_retrieve_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        response = self.client.get(url)
        expected_data = ProfileSerializer(self.profile).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_data, response.data)
        
    def test_retrieve_unauthorized_forbidden_access(self):
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_retrieve_missing_pk_for_specific_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": 2317823178231})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_successful_profile_patch_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Test Description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_not_authenticated_patch(self):
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Test Description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_not_allowed_to_patch_profile(self):
        self.user_two = User.objects.create_user(username="testusertwo", password="testpassword123", email="testmailtwo@mail.com")
        self.client.force_authenticate(user=self.user_two)
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Test Description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_patch_profile_not_found(self):
        url = reverse("profile-detail", kwargs={"pk": 214123123})
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Test Description",
            "working_hours": "10-18",
            "email": "new_email@business.de"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_patch_email_not_unique(self):
        self.user_two = User.objects.create_user(username="testusertwo", password="testpassword123", email="testmailtwo@mail.com")
        self.client.force_authenticate(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Test Description",
            "working_hours": "10-18",
            "email": "testmailtwo@mail.com"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_patch_email_is_unique(self):
        self.user_two = User.objects.create_user(username="testusertwo", password="testpassword123", email="testmailtwo@mail.com")
        self.client.force_authenticate(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Test Description",
            "working_hours": "10-18",
            "email": "thisisauniquemail@mail.com"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)