from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user.profile.type == "business":
                return True
        return False