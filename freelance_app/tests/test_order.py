from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from auth_app.models import UserProfile
from freelance_app.models import Offer, OfferDetail, Order


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123", email="testmail@mail.com")
        self.profile = UserProfile.objects.create(
            user=self.user, type="customer")
        self.user_two = User.objects.create_user(
            username="testusertwo", password="testpassword123", email="testmailtwo@mail.com", is_staff=True)
        self.profile_two = UserProfile.objects.create(
            user=self.user_two, type="business")
        self.offer = Offer.objects.create(
            user=self.user, title="Test", description="Test")
        self.offer_detail = OfferDetail.objects.create(offer=self.offer, title="Test",
                                                       revisions=2,
                                                       delivery_time_in_days=5, price=100,
                                                       features=[
                                                           "Test1", "Test2"],
                                                       offer_type="basic"
                                                       )
        self.order = Order.objects.create(customer_user=self.user, offer_detail_id=1)

    def test_post_order_successful(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-list")
        data = {
            "offer_detail_id": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_missing_order_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-list")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_not_authenticated(self):
        url = reverse("order-list")
        data = {
            "offer_detail_id": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_not_customer(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("order-list")
        data = {
            "offer_detail_id": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_successful(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_not_authenticated(self):
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order_successful(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_order_wrong_status(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        data = {
            "status": "almost_completed"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_not_authenticated(self):
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order_not_business_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_not_found(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("order-detail", kwargs={"pk": 210210210210})
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_successful(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_not_authenticated(self):
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_order_user_not_staff(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-detail", kwargs={"pk": self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_not_found(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("order-detail", kwargs={"pk": 3098321098})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)