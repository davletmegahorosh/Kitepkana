from rest_framework import permissions
from .utils import user_authenticate
"""Переопределяем встроенные классы. Данные классы определяют права доступа"""
#
HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
USER_METHODS = HTTP_METHODS[0:3]


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view,):
        return user_authenticate(request=request, http_methods=USER_METHODS)


class IsAdminOnly(IsAuthenticated):
    def has_permission(self, request, view,):
        return user_authenticate(request=request, http_methods=HTTP_METHODS)



