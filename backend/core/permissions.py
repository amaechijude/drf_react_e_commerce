from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVendor(BasePermission):
    """
    Allows access only to vendor users.
    """

    def has_permission(self, request, view):
        message = "User is not a vendor"
        return bool(request.user and hasattr(request.user, 'is_vendor') and request.user.is_vendor)