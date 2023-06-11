from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPostOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request method is safe (e.g., GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        return obj.user == request.user