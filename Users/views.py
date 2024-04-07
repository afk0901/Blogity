"""This module contains view-sets for CRUD operations for the User of the
posts, comments etc."""

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from Permissions.user_permissions import UserOnlyModifyOwnAllowRead
from Users.models import CustomUser
from Users.serializers import UserSerializer


@extend_schema(
    methods=["GET"], description="Retrieve a list of users or a specific user by ID"
)
@extend_schema(
    methods=["POST"], description="Create a specific user and add the user to the list"
)
@extend_schema(methods=["PUT"], description="Update a specific user")
class UserViewSet(viewsets.ModelViewSet):
    """Endpoint for viewing and editing users."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "put"]
    permission_classes = [UserOnlyModifyOwnAllowRead]
