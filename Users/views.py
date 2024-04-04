"""This module contains view-sets for CRUD operations for the User of the
posts, comments etc."""

from rest_framework import viewsets

from Permissions.user_permissions import UserOnlyModifyOwnAllowRead
from Users.models import CustomUser
from Users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Endpoint for viewing and editing users.

    Supported methods: GET, POST, PUT

    Get Operations:
    - /: Returns a list of all users in the system.
    - /<id>: Returns a specific user by id

    Post Operations:
    - /: Adds a new user to the system

    Put Operations:
    - /<id>: Updates a specific user

    Delete Operations:
    - /<id>: Deletes a specific user

    Note: Pagination will be implemented in a future update.

    Query Parameters: None.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "put"]
    permission_classes = [UserOnlyModifyOwnAllowRead]
