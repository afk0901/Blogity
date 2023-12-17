from django.contrib.auth import get_user_model
from rest_framework import serializers
from Users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    User = get_user_model()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "password"]

    def create(self, validated_data):
        # Ensuring the password will be hashed. The serializer does not do so be default.
        # Note to self: No value in unit test this as it would only test the mock (user).
        # There is no control logic.
        user = self.User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Ensuring the password will be hashed. The serializer does not do so be default.
        # Same here regarding testing as in the create method.
        instance.set_password(validated_data['password'])
        return instance
