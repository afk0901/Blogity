from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField

from Users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "password"]

    def create(self, validated_data) -> CustomUser:
        # Ensuring the password will be hashed. The serializer does not do so be default.
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data) -> CustomUser:
        # Ensuring the password will be hashed. The serializer does not do so be default.
        # Same here regarding testing as in the create method.
        super().update(instance, validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
