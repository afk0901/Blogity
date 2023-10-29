from django.shortcuts import render
from rest_framework import viewsets
from Users.models import CustomUser
from Users.serializers.UserSerializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
