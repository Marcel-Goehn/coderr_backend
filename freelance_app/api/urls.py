from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferModelViewSet, OfferDetailModelViewSet

router = DefaultRouter()
router.register(r"offers", OfferModelViewSet, basename="offer")
router.register(r"offerdetail", OfferDetailModelViewSet, basename="offerdetail")

urlpatterns = [
    path("", include(router.urls))
]