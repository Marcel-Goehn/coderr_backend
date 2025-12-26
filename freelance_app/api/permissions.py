from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            if request.user.profile.type == "business":
                return True
        return False