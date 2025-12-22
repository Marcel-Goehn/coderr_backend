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
        
    def test_unauthorized_forbidden_access(self):
        url = reverse("profile-detail", kwargs={"pk": self.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_missing_pk_for_specific_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": 2317823178231})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)