from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferModelViewSet

router = DefaultRouter()
router.register(r"offers", OfferModelViewSet, basename="offer")

urlpatterns = [
    path("", include(router.urls))
]