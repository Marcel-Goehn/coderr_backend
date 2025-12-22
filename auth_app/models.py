from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):

    user_choices = [
        ("customer", "customer"),
        ("business", "business"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/", blank=True)
    location = models.CharField(max_length=20, blank=True)
    telephone_number = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=100, blank=True)
    working_hours = models.CharField(max_length=10, blank=True)
    user_type = models.CharField(max_length=10, choices=user_choices)
    
