from django.contrib.auth.models import User
from django.db.models import Min
from rest_framework import serializers
from freelance_app.models import Offer, OfferDetail


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
        offer = Offer.objects.create(title=validated_data["title"], description=validated_data["description"], user=validated_data["user"])
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
        read_only_fields = ["id", "url"]


class OfferGetListSerializer(serializers.ModelSerializer):

    details = OfferDetailHyperLinkedSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField(read_only=True)
    min_delivery_time = serializers.SerializerMethodField(read_only=True)
    user_details = UserDetailSerializer(source="user", read_only=True)

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "details", "min_price", "min_delivery_time", "user_details"]
        read_only_fields = ["id", "user", "title", "image", "description", "created_at", "updated_at"]

    def get_min_price(self, object):
        aggregated_price = object.details.aggregate(Min("price"))
        return aggregated_price["price__min"]

    def get_min_delivery_time(self, object):
        aggregated_delivery_time_in_days =  object.details.aggregate(Min("delivery_time_in_days"))
        return aggregated_delivery_time_in_days["delivery_time_in_days__min"]