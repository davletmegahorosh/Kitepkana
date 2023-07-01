from rest_framework import permissions


class IsAdminOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)

## Нужно внести этот код на сервер
class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if obj.profile.user == request.user:
            return True
        if obj.user == request.user:
            return True
            # return bool(obj.user == request.user)

# ---