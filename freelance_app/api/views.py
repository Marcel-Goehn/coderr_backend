from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import OfferPostSerializer, OfferGetListSerializer, OfferDetailHyperLinkedSerializer
from .permissions import IsBusinessUser
from freelance_app.models import Offer, OfferDetail


class OfferModelViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, IsBusinessUser]

    def get_serializer_class(self):
        if self.action == "list":
            return OfferGetListSerializer
        elif self.action == "create":
            return OfferPostSerializer
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "list":
            context["request"] = None
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailModelViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailHyperLinkedSerializer