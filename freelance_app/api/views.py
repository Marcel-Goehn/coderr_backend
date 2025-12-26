from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import OfferSerializer
from .permissions import IsBusinessUser
from freelance_app.models import Offer


class OfferModelViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]