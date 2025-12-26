from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from auth_app.models import UserProfile


class OfferTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword123", email="testmail@mail.com")
        self.profile = UserProfile.objects.create(user=self.user, type="business")

    def test_post_offer_successful(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("offer-list")
        data = {
                "title": "Grafikdesign-Paket",
                "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
                "details": [
                    {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                                "Logo Design",
                                "Visitenkarte"
                    ],
                    "offer_type": "basic"
                    },
                    {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                                "Logo Design",
                                "Visitenkarte",
                                "Briefpapier"
                    ],
                    "offer_type": "standard"
                    },
                    {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                                "Logo Design",
                                "Visitenkarte",
                                "Briefpapier",
                                "Flyer"
                    ],
                    "offer_type": "premium"
                    }
                ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_offer_not_authenticated(self):
        url = reverse("offer-list")
        data = {
                "title": "Grafikdesign-Paket",
                "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
                "details": [
                    {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                                "Logo Design",
                                "Visitenkarte"
                    ],
                    "offer_type": "basic"
                    },
                    {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                                "Logo Design",
                                "Visitenkarte",
                                "Briefpapier"
                    ],
                    "offer_type": "standard"
                    },
                    {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                                "Logo Design",
                                "Visitenkarte",
                                "Briefpapier",
                                "Flyer"
                    ],
                    "offer_type": "premium"
                    }
                ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_offer_not_business_type(self):
        self.user_two = User.objects.create_user(username="usernametwo", password="testpassword123", email="testmailer@gmailer.com")
        self.profile_two = UserProfile.objects.create(user=self.user_two, type="customer")
        self.client.force_authenticate(user=self.user_two)
        url = reverse("offer-list")
        data = {
                "title": "Grafikdesign-Paket",
                "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
                "details": [
                    {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                                "Logo Design",
                                "Visitenkarte"
                    ],
                    "offer_type": "basic"
                    },
                    {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                                "Logo Design",
                                "Visitenkarte",
                                "Briefpapier"
                    ],
                    "offer_type": "standard"
                    },
                    {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                                "Logo Design",
                                "Visitenkarte",
                                "Briefpapier",
                                "Flyer"
                    ],
                    "offer_type": "premium"
                    }
                ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_offer_not_three_details(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("offer-list")
        data = {
                "title": "Grafikdesign-Paket",
                "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
                "details": [
                    {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                                "Logo Design",
                                "Visitenkarte"
                    ],
                    "offer_type": "basic"
                    },
                    {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                                "Logo Design",
                                "Visitenkarte",
                                "Briefpapier"
                    ],
                    "offer_type": "standard"
                    }
                ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        