"""
This module provides custom permissions for the user.
What operations the user can perform on other users
or herself/himself
"""

from rest_framework import permissions


class CanModifyUser(permissions.BasePermission):
    """
    Permission to modify the user.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.method == 'GET'
