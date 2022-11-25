from rest_framework.permissions import BasePermission


"""class IsDean(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return bool(request.user.status == "DEAN")"""
