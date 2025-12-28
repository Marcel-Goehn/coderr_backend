from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (OfferPostSerializer, OfferGetListSerializer,
                          OfferDetailHyperLinkedSerializer, OfferRetrieveSerializer,
                          OfferPatchSerializer)
from .permissions import IsBusinessUser
from freelance_app.models import Offer, OfferDetail
from rest_framework import filters
from .paginations import OfferListPagination
from django.db.models import Min


class OfferModelViewSet(viewsets.ModelViewSet):
    pagination_class = OfferListPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]

    def get_queryset(self):
        if self.action == "create":
            return Offer.objects.all()
        elif self.action == "retrieve":
            qs = Offer.objects.all()
            annotated_qs = qs.annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days")
            )
            return annotated_qs
        elif self.action == "list":
            qs = Offer.objects.all()
            annotated_qs = qs.annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days"),
                )
            min_price_query_param = self.request.query_params.get("min_price")
            creator_id_query_param = self.request.query_params.get("creator_id")
            max_delivery_time_query_param = self.request.query_params.get("max_delivery_time")

            if min_price_query_param is not None:
                annotated_qs = annotated_qs.filter(min_price__gte=min_price_query_param)
            if creator_id_query_param is not None:
                annotated_qs = annotated_qs.filter(user__pk=creator_id_query_param)
            if max_delivery_time_query_param is not None:
                annotated_qs = annotated_qs.filter(min_delivery_time__lte=max_delivery_time_query_param)
            return annotated_qs
        elif self.action == "partial_update":
            return Offer.objects.all()
        elif self.action == "destroy":
            return Offer.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OfferGetListSerializer
        elif self.action == "retrieve":
            return OfferRetrieveSerializer
        elif self.action == "create":
            return OfferPostSerializer
        elif self.action == "partial_update":
            return OfferPatchSerializer
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "list":
            context["request"] = None
        return context
    
    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.action == "retrieve":
            return [IsAuthenticated()]
        if self.action == "partial_update":
            return [IsAuthenticated(), IsBusinessUser()]
        if self.action == "destroy":
            return [IsAuthenticated(), IsBusinessUser()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailModelViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailHyperLinkedSerializer