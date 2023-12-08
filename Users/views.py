from rest_framework import viewsets

from Users.models import CustomUser
from Users.serializers import UserSerializer
from Permissions.user_permissions import UserOnlyModifyOwnAllowRead


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [UserOnlyModifyOwnAllowRead]
    