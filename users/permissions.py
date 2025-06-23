from rest_framework import permissions


class IsModeratorReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.groups.filter(name="Модераторы").exists():
            return request.method in permissions.SAFE_METHODS

        return True
