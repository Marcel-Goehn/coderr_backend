from rest_framework import serializers
from freelance_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", 
                  "price", "features", "offer_type"]
        read_only_fields = ["id"]


class OfferSerializer(serializers.ModelSerializer):

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
        offer = Offer.objects.create(title=validated_data["title"], description=validated_data["description"])
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
