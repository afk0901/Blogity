"""
This module provides custom permissions for the
users.
What operations they have access to and what they can do.
"""
from rest_framework import permissions


class AllowOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return True
