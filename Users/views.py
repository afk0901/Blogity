from django.shortcuts import render
from rest_framework import viewsets
from Users.models import CustomUser
from Users.serializers.UserSerializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
