from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request method is safe (e.g., GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated and request.user.is_moderator:
            return True

        # Otherwise, the user does not have permission to edit
        return False
