from rest_framework import serializers
from freelance_app.models import Offer, OfferDetail, OfferDetailFeature


class OfferDetailFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetailFeature
        fields = ["feature"]


class OfferDetailSerializer(serializers.ModelSerializer):

    features = OfferDetailFeatureSerializer(many=True)

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

    def create(self, validated_data):
        print(validated_data)