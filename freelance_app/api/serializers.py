from django.contrib.auth.models import User
from rest_framework import serializers
from freelance_app.models import Offer, OfferDetail, Order, Review
from django.shortcuts import get_object_or_404


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", 
                  "price", "features", "offer_type"]
        read_only_fields = ["id"]


class OfferPostSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta: 
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("A offer must contain three offer details.")
        return value

    def create(self, validated_data):
        offer = Offer.objects.create(title=validated_data["title"], 
                                     description=validated_data["description"], 
                                     user=validated_data["user"])
        for detail in validated_data["details"]:
            OfferDetail.objects.create(
                offer=offer, 
                title=detail["title"], 
                revisions=detail["revisions"], 
                delivery_time_in_days=detail["delivery_time_in_days"],
                price=detail["price"],
                features=detail["features"],
                offer_type=detail["offer_type"])
        return offer
    

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]
        read_only_fields = ["first_name", "last_name", "username"]


class OfferDetailHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]
        extra_kwargs = {
            "url": {
                "view_name": "offerdetail",
                "lookup_field": "pk",
                "read_only": True
            }
        }


class OfferGetListSerializer(serializers.ModelSerializer):

    details = OfferDetailHyperLinkedSerializer(many=True, read_only=True)
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()
    user_details = UserDetailSerializer(source="user", read_only=True)

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", 
                  "updated_at", "details", "min_price", "min_delivery_time", 
                  "user_details"]
        read_only_fields = ["id", "user", "title", "image", "description", 
                            "created_at", "updated_at"]
        

class OfferRetrieveSerializer(serializers.ModelSerializer):

    details = OfferDetailHyperLinkedSerializer(many=True, read_only=True)
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at",
                  "updated_at", "details", "min_price", "min_delivery_time"]
        read_only_fields = ["id", "user", "title", "image", "description", "created_at",
                            "updated_at"]
        

class OfferPatchSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]

    def validate_details(self, value):
        if value is not None:
            for single_detail_offer in value:
                features = single_detail_offer.get("features", None)
                if features and type(features) is not list:
                    raise serializers.ValidationError("features have to be in a list.")
                if "offer_type" not in single_detail_offer:
                    raise serializers.ValidationError("offer_type has to be entered to access the right offer detail.")
        return value

    def update(self, instance, validated_data):
        offer_details = validated_data.pop("details", None)
        if offer_details is not None:
            for detail in offer_details:
                single_offer_detail = OfferDetail.objects.get(offer=instance, offer_type=detail["offer_type"])
                single_offer_detail.title = detail.get("title", single_offer_detail.title)
                single_offer_detail.revisions = detail.get("revisions", single_offer_detail.revisions)
                single_offer_detail.delivery_time_in_days = detail.get("delivery_time_in_days", single_offer_detail.delivery_time_in_days)
                single_offer_detail.price = detail.get("price", single_offer_detail.price)
                single_offer_detail.features = detail.get("features", single_offer_detail.features)
                single_offer_detail.save()

        instance.title = validated_data.get("title", instance.title)
        instance.image = validated_data.get("image", instance.image)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
    

class OrderPostSerializer(serializers.ModelSerializer):

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(),
        write_only=True,
        source="offer_detail"
    )
    business_user = serializers.IntegerField(source="offer_detail.offer.user.id", read_only=True)
    title = serializers.CharField(source="offer_detail.title", max_length=50, read_only=True)
    revisions = serializers.IntegerField(source="offer_detail.revisions", read_only=True)
    delivery_time_in_days = serializers.IntegerField(source="offer_detail.delivery_time_in_days", read_only=True)
    price = serializers.FloatField(source="offer_detail.price", read_only=True)
    features = serializers.JSONField(source="offer_detail.features", read_only=True)
    offer_type = serializers.CharField(source="offer_detail.offer_type", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "offer_detail_id", "customer_user", "business_user", 
                  "title", "revisions", "delivery_time_in_days", "price", "features", 
                  "offer_type", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]
        extra_kwargs = {
            "customer_user": {"required": False}
        }


class OrderListUpdateSerializer(serializers.ModelSerializer):

    business_user = serializers.IntegerField(source="offer_detail.offer.user.id", read_only=True)
    title = serializers.CharField(source="offer_detail.title", max_length=50, read_only=True)
    revisions = serializers.IntegerField(source="offer_detail.revisions", read_only=True)
    delivery_time_in_days = serializers.IntegerField(source="offer_detail.delivery_time_in_days", read_only=True)
    price = serializers.FloatField(source="offer_detail.price", read_only=True)
    features = serializers.JSONField(source="offer_detail.features", read_only=True)
    offer_type = serializers.CharField(source="offer_detail.offer_type", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_user", "business_user", "title", "revisions",
                   "delivery_time_in_days", "price", "features", "offer_type", 
                   "status", "created_at", "updated_at"]
        read_only_fields = ["id", "customer_user", "created_at", "updated_at"]


class ReviewListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate_business_user(self, value):
        if value.profile.type == "customer":
            raise serializers.ValidationError("You can't give a review to a customer.")
        return value

    def validate(self, data):
        all_reviews_for_business_user = Review.objects.filter(business_user=data["business_user"])
        if all_reviews_for_business_user.filter(reviewer=self.context["request"].user).exists():
            raise serializers.ValidationError({"reviewer": "You already gave this seller a review."})
        return data
    

class ReviewPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "business_user", "reviewer", "created_at", "updated_at"]