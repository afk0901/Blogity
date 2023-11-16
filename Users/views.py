from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from Users.models import CustomUser
from Users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [AllowAny]
    