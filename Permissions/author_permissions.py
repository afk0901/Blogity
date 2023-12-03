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
    to modify the object or create a new object,
    For example, author of a post or a comment.

    GET requests will always pass as anybody can read the object.
    """

    def has_permission(self, request, view):
        """
        Preventing the user to create a POST for another author than
        themselves.
        On list level as this adds to the list if permission is granted.

        :param request: The incoming request object
        :param view: The view we are working with
        :return: True if user is the author of the object,
        granting permission, otherwise False, not granting
        permissions.
        """
        # request only has the data attribute if it's a POST request
        if hasattr(request, 'data'):
            if 'author' in request.data:
                # bool(request.user and request.user.is_authenticated)
                return request.data["author"] == request.user.id
        return True

    def has_object_permission(self, request, view, obj):
        """
        Preventing a user that is not the author of an object,
        to modify the object.

        GET requests will always pass the check as anybody can read
        the object.

        :param request: The incoming request object
        :param view: The view we are working with
        :param obj: Object that has an author attribute
        :return: True if user is the author of the object,
        granting permission, otherwise False, not granting
        permissions.
        """

        # Allow GET requests without authorization
        if request.method == 'GET':
            return True
        else:
            return obj.author == request.user
