"""
This module provides custom permissions for the
users.
What operations they have access to and what they can do.
"""
from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """
    The object must contain the author attribute.

    Custom permission that only allows an author of the object
    to perform CRUD on that object.
    For example, author of a post or a comment.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
