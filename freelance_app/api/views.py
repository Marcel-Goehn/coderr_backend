from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import OfferSerializer
from freelance_app.models import Offer


class OfferModelViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [AllowAny]