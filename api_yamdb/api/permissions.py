from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import User


class IsAdmin(BasePermission):
    """
    Read /write permissions has only
    site admin or Django administrator.
    """
    def has_permission(self, request, view):
        user = request.user
        is_admin = (request.user.is_authenticated
                    and request.user.role == User.ADMIN)
        is_superuser = user.is_superuser
        return is_admin or is_superuser


class IsAdminOrReadOnly(BasePermission):
    """
    Read permission for safe methods
    or user is authenticated and has admins role.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == User.ADMIN:
            return True
        return request.user.is_superuser


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):
    """
    Read permissions for all
    write permissions has author, admin, moderator and superuser.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user == obj.author:
            return True
        if request.user.role in (User.ADMIN, User.MODERATOR):
            return True
        return request.user.is_superuser
