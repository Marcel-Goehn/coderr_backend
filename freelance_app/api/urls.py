from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferModelViewSet, OfferDetailRetrieveView, OrderListCreateView, OrderUpdateDestroyView

router = DefaultRouter()
router.register(r"offers", OfferModelViewSet, basename="offer")

urlpatterns = [
    path("", include(router.urls)),
    path("offerdetails/<int:pk>/", OfferDetailRetrieveView.as_view(), name="offerdetail"),
    path("orders/", OrderListCreateView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderUpdateDestroyView.as_view(), name="order-detail")
]