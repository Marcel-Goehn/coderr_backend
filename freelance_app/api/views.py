from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (OfferPostSerializer, OfferGetListSerializer, OfferRetrieveSerializer,
                          OfferPatchSerializer, OfferDetailSerializer, OrderPostSerializer,
                          OrderListUpdateSerializer, ReviewListCreateSerializer)
from .permissions import CustomOfferPermissions, CustomOrderPermissions, CustomReviewPermission
from freelance_app.models import Offer, OfferDetail, Order, Review
from rest_framework import filters
from .paginations import OfferListPagination
from django.db.models import Min
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response


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
            creator_id_query_param = self.request.query_params.get(
                "creator_id")
            max_delivery_time_query_param = self.request.query_params.get(
                "max_delivery_time")

            if min_price_query_param is not None:
                annotated_qs = annotated_qs.filter(
                    min_price__gte=min_price_query_param)
            if creator_id_query_param is not None:
                annotated_qs = annotated_qs.filter(
                    user__pk=creator_id_query_param)
            if max_delivery_time_query_param is not None:
                annotated_qs = annotated_qs.filter(
                    min_delivery_time__lte=max_delivery_time_query_param)
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
            return [IsAuthenticated(), CustomOfferPermissions()]
        if self.action == "retrieve":
            return [IsAuthenticated()]
        if self.action == "partial_update":
            return [IsAuthenticated(), CustomOfferPermissions()]
        if self.action == "destroy":
            return [IsAuthenticated(), CustomOfferPermissions()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, CustomOrderPermissions]

    def get_queryset(self):
        if self.request.method == "GET":
            return Order.objects.filter(Q(customer_user__id=self.request.user.id) | Q(offer_detail__offer__user__id=self.request.user.id))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderListUpdateSerializer
        if self.request.method == "POST":
            return OrderPostSerializer

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)


class OrderUpdateDestroyView(mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             generics.GenericAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderListUpdateSerializer
    permission_classes = [IsAuthenticated, CustomOrderPermissions]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OrderCountInProgressView(APIView):
    def get(self, req, pk):
        user = get_object_or_404(User, pk=pk)
        if user.profile.type != "business":
            return Response("User is not of type business.", status=status.HTTP_404_NOT_FOUND)
        queryset_count = Order.objects.filter(
            offer_detail__offer__user__pk=user.pk, status="in_progress").count()
        data = {
            "order_count": queryset_count
        }
        return Response(data, status=status.HTTP_200_OK)


class OrderCountCompleted(APIView):
    def get(self, req, pk):
        user = get_object_or_404(User, pk=pk)
        if user.profile.type != "business":
            return Response("User is not of type business.", status=status.HTTP_404_NOT_FOUND)
        queryset_count = Order.objects.filter(
            offer_detail__offer__user__pk=user.pk, status="completed").count()
        data = {
            "order_count": queryset_count
        }
        return Response(data, status=status.HTTP_200_OK)
    

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListCreateSerializer
    permission_classes = [IsAuthenticated, CustomReviewPermission]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
