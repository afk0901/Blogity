"""Provides custom permissions for the user.

Determining what operations the user can perform on any user data and what information
they can access about other users.

The primary goal is to ensure users can modify only their own information while allowing
them to read others' public data.
"""

from rest_framework import permissions


class UserOnlyModifyOwnAllowRead(permissions.BasePermission):
    """A permission class that allows a user to modify their own information
    but provides read access to all users.

    This custom permission class ensures that a user has the ability to
    update or delete their own data while allowing them to view (GET
    request) data of other users and prevent the user from modifying
    unauthorized user data.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        """Check if the request should be permitted on a specific user data
        object.

        Allows read access to any request (GET method).
        Write access is only permitted if the user making the request is the same as
        the user object the request is trying to modify.

        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        # Allow read access for any request
        # Write permissions are only allowed to the user itself
        return bool(request.user == obj or request.method in permissions.SAFE_METHODS)
