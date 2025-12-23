from django.urls import path
from .views import RegistrationView, LoginView, ProfileRetrievePatchView, ProfileListView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/<int:pk>/", ProfileRetrievePatchView.as_view(), name="profile-detail"),
    path("profiles/business/", ProfileListView.as_view(), name="business-profile-list"),
    path("profiles/customer/", ProfileListView.as_view(), name="customer-profile-list")
]