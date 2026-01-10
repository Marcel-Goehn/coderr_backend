from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from auth_app.models import UserProfile
from freelance_app.models import Offer, OfferDetail, Order


class ReviewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123", email="testmail@mail.com")
        self.profile = UserProfile.objects.create(
            user=self.user, type="customer")
        self.user_two = User.objects.create_user(
            username="testusertwo", password="testpassword123", email="testmailtwo@mail.com", is_staff=True)
        self.profile_two = UserProfile.objects.create(
            user=self.user_two, type="business")
        self.user_three = User.objects.create_user(
            username="testuserthree", password="testpassword123", email="testmailthree@mail.com")
        self.profile_three = UserProfile.objects.create(
            user=self.user_three, type="customer")
        self.user_four = User.objects.create_user(
            username="testuserfour", password="testpassword123", email="testmailfour@mail.com")
        self.profile_four = UserProfile.objects.create(
            user=self.user_four, type="business")
        self.offer = Offer.objects.create(
            user=self.user, title="Test", description="Test")
        self.offer_detail = OfferDetail.objects.create(offer=self.offer, title="Test",
                                                       revisions=2,
                                                       delivery_time_in_days=5, price=100,
                                                       features=[
                                                           "Test1", "Test2"],
                                                       offer_type="basic"
                                                       )
        self.order = Order.objects.create(
            customer_user=self.user, offer_detail_id=1)

    def test_post_review_successful(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("review-list")
        data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_review_already_received_review(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("review-list")
        data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        second_response = self.client.post(url, data, format="json")
        self.assertEqual(second_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_post_review_not_authenticated(self):
        url = reverse("review-list")
        data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_review_not_business_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("review-list")
        data = {
            "business_user": 3,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_review_logged_in_user_is_business_user(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("review-list")
        data = {
            "business_user": 4,
            "rating": 4,
            "description": "Alles war toll!"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_review_list_successful(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("review-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_review_list_not_authenticated(self):
        url = reverse("review-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)