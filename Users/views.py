"""This module contains view-sets for CRUD operations for the User of the posts, comments etc."""

from rest_framework import viewsets

from Permissions.user_permissions import UserOnlyModifyOwnAllowRead
from Users.models import CustomUser
from Users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """General user viewset, enables creation, update and read for the CustomUser model and represents it on read."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "put"]
    permission_classes = [UserOnlyModifyOwnAllowRead]
