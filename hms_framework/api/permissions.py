from rest_framework import permissions


class IsAdminOrUserReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        is_authenticated = bool(request.user and request.user.is_authenticated)
        return is_admin or (is_authenticated and request.method in permissions.SAFE_METHODS)


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsManagement(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='IsManagement').first())


class IsSuperUserOrAdminReadOnly(IsSuperUser):
    def has_permission(self, request, view):
        is_super_user = super().has_permission(request, view)
        if is_super_user:
            return True
        is_admin = permissions.IsAdminUser().has_permission(request, view)
        return is_admin and request.method in permissions.SAFE_METHODS


class IsSuperUserOrManagementReadOnly(IsSuperUser):
    def has_permission(self, request, view):
        is_super_user = super().has_permission(request, view)
        if is_super_user:
            return True
        is_admin = permissions.IsAdminUser().has_permission(request, view)
        if is_admin:
            return is_admin and request.method in permissions.SAFE_METHODS
        is_management = IsManagement().has_permission(request, view)
        return is_management and request.method in permissions.SAFE_METHODS


class IsSuperUserOrUserReadOnly(IsSuperUser):
    def has_permission(self, request, view):
        is_super_user = super().has_permission(request, view)
        if is_super_user:
            return True
        is_authenticated = permissions.IsAuthenticated().has_permission(request, view)
        return is_authenticated and request.method in permissions.SAFE_METHODS
