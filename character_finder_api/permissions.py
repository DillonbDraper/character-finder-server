from rest_framework import permissions

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'update' or view.action == 'partial_update':
            return request.user.is_staff is True
        elif view.action == 'destroy':
            return request.user.is_staff is True
        elif view.action in ['retrieve', 'list', 'create']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_active:
            return False
        if view.action in ['list', 'retrieve', 'create']:
            return request.user.is_active
        elif view.action in ['update', 'partial_update', 'destroy']:
            return obj == request.user or request.user.is_staff
        else:
            return False
