"""This module provides custom permissions for the users.

What operations they have access to and what they can do.
"""

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from Posts.models import Comment, Post


class IsAuthorAnyRead(permissions.BasePermission):
    """The object must contain the author attribute.

    Custom permission that only allows an author of the object to modify the object or
    create a new object.

    GET requests will always pass as anybody can read the object.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Preventing the user to create a POST for another author than
        themselves.

        On list level as this adds to the list if permission is granted.

        :param request: The incoming request object
        :param view: The view we are working with
        :return: True if user is the author of the object, granting permission,
            otherwise False, not granting permissions.
        """

        if request.method == "POST":
            # Casting to prevent type mismatch.
            return hasattr(request.user, "id") and str(
                request.data.get("author_id")
            ) == str(request.user.id)
        return True

    def has_object_permission(
        self, request: Request, view: APIView, obj: Post | Comment
    ) -> bool:
        """Preventing a user that is not the author of an object, to modify the
        object.

        GET requests will always pass the check as anybody can read the object.

        :param request: The incoming request object
        :param view: The view we are working with
        :param obj: Object that has an author attribute
        :return: True if user is the author of the object, granting permission,
            otherwise False, not granting permissions. Ensuring that the user can't
            change the id of author attribute and therefore make post as another user.
        """
        if request.method == "GET":
            return True
        else:
            # Casting to prevent type mismatch.
            return hasattr(request.user, "id") and str(obj.author_id) == str(
                request.user.id
            )
