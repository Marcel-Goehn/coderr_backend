from rest_framework import permissions


class CustomOfferPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            if request.user.profile.type == "business":
                return True
        
        if request.method == "PATCH":
            return True
        
        if request.method == "DELETE":
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == "PATCH":
            return request.user == obj.user
        
        if request.method == "DELETE":
            return request.user == obj.user
        

class CustomOrderPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            return request.user.profile.type == "customer"
        
        if request.method == "PATCH":
            return request.user.profile.type == "business"
        
        if request.method == "DELETE":
            return request.user.is_staff

        return False


class CustomReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.profile.type == "customer"
        if request.method == "PATCH":
            return True
        if request.method == "DELETE":
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            return request.user.id == obj.reviewer.id
        if request.method == "DELETE":
            return request.user.id == obj.reviewer.id
        return False