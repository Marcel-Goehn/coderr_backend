from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        if request.method == "PATCH":
            return request.user == obj.user
