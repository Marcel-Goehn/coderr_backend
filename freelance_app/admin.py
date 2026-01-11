from django.contrib import admin
from .models import Offer, OfferDetail, Order, Review

# Register your models here.


admin.site.register(Offer)
admin.site.register(OfferDetail)
admin.site.register(Order)
admin.site.register(Review)


