from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offer")
    title = models.CharField(max_length=50)
    image = models.FileField(upload_to="offers/", blank=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title}"


class OfferDetail(models.Model):

    offer_choices = [
        ("basic", "basic"),
        ("standard", "standard"),
        ("premium", "premium")
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=50)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.FloatField()
    offer_type = models.CharField(max_length=10, choices=offer_choices)

    def __str__(self):
        return f"{self.title}"
    

class OfferDetailFeature(models.Model):
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name="features")
    feature = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.feature}"
