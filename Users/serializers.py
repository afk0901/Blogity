from django.contrib.auth import get_user_model
from rest_framework import serializers
from Users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    User = get_user_model()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "password"]

    def create(self, validated_data):
        user = self.User.objects.create_user(**validated_data)
        return user

    #TODO: Implement Put so that the password does get hashed




