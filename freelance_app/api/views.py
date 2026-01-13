from django.db.models import Q, Min, Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import viewsets, status, generics, mixins, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import (OfferPostSerializer, OfferGetListSerializer, OfferRetrieveSerializer,
                          OfferPatchSerializer, OfferDetailSerializer, OrderPostSerializer,
                          OrderListUpdateSerializer, ReviewListCreateSerializer,
                          ReviewPatchSerializer)
from .permissions import CustomOfferPermissions, CustomOrderPermissions, CustomReviewPermission
from freelance_app.models import Offer, OfferDetail, Order, Review
from auth_app.models import UserProfile
from .paginations import OfferListPagination


class OfferModelViewSet(viewsets.ModelViewSet):
    """
    This view offers the ability to use pagination, the search filter and the ordering filter.
    The information about the pagination can be found in paginations.py
    """

    pagination_class = OfferListPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]

    def get_queryset(self):
        """
        If the action is "list", you have the ability to use the query parameters.
        It will check if they are present in the query params, and if they are it will
        filter with their help.
        """
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

            if max_delivery_time_query_param is not None:
                try:
                    max_delivery_time_query_param = int(
                        max_delivery_time_query_param)
                except ValueError:
                    raise ValidationError(
                        {"max_delivery_time": "Has to be an integer."})

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
        """
        It has to return None. The idea behind it is, 
        that in the response there will be a relative path to the offer details,
        instead of an absolute one.
        """
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
            return Order.objects.filter(Q(customer_user__id=self.request.user.id) |
                                        Q(offer_detail__offer__user__id=self.request.user.id))

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
    """
    Returns an overall count of all orders that belong to a specific business user and
    have the status of in_progress.
    """

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
    """
    Returns an overall count of all orders that belong to a specific business user and
    have the status of completed.
    """

    def get(self, req, pk):
        user = get_object_or_404(User, pk=pk)
        if user.profile.type != "business":
            return Response("User is not of type business.", status=status.HTTP_404_NOT_FOUND)
        queryset_count = Order.objects.filter(
            offer_detail__offer__user__pk=user.pk, status="completed").count()
        data = {
            "completed_order_count": queryset_count
        }
        return Response(data, status=status.HTTP_200_OK)


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    This view offers the ability to use ordering and filtering via query parameters
    """

    serializer_class = ReviewListCreateSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']

    def get_queryset(self):
        """
        If the request is a GET method, the queryset will be filtered with the help of 
        query parameters, if they are present.
        """
        if self.request.method == "POST":
            return Review.objects.all()
        elif self.request.method == "GET":
            qs = Review.objects.all()
            business_user_id = self.request.query_params.get(
                "business_user_id", None)
            reviewer_id = self.request.query_params.get("reviewer_id", None)
            if business_user_id is not None:
                qs = qs.filter(business_user__id=business_user_id)
            if reviewer_id is not None:
                qs = qs.filter(reviewer__id=reviewer_id)
            return qs

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsAuthenticated(), CustomReviewPermission()]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ReviewPatchDeleteView(mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewPatchSerializer
    permission_classes = [IsAuthenticated, CustomReviewPermission]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BaseInformationView(APIView):
    permission_classes = [AllowAny]

    def get(self, req):
        """
        Returns an overall base information about the platform.
        """
        reviews = Review.objects.all()
        business_profiles = UserProfile.objects.filter(type="business")
        offers = Offer.objects.all()
        average_rating_dict = reviews.aggregate(Avg("rating"))
        average_rating = average_rating_dict.get("rating__avg")
        if average_rating == None:
            average_rating = 0.0
        data = {
            "review_count": reviews.count(),
            "average_rating": float((f"{average_rating:.1f}")),
            "business_profile_count": business_profiles.count(),
            "offer_count": offers.count()
        }
        return Response(data)
