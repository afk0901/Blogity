from rest_framework import viewsets

from Permissions.user_permissions import UserOnlyModifyOwnAllowRead
from Users.models import CustomUser
from Users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "put"]
    permission_classes = [UserOnlyModifyOwnAllowRead]
