"""
This module defines a Django Rest Framework serializer for the CustomUser model.

Facilitates the serialization and deserialization of user data.

It is specifically designed to handle user creation and updates within a Django
application, with a strong emphasis on security.

By hashing passwords both when creating new users and updating existing ones,
it ensures that sensitive information is adequately protected.
"""

from rest_framework import serializers
from Users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for the CustomUser model.

    This serializer handles the serialization and deserialization of CustomUser instances,
    ensuring secure password handling by hashing passwords upon creation and update.
    """

    # Using CharField with write_only=True for password handling to ensure it's never sent back to the client.
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        Metaclass configuration for UserSerializer with password.

        Specifies the model it is associated with and the fields that should be
        included in the serialized representation.
        The inclusion of the password field with write_only=True ensures it is used
        for creating or updating instances but not returned in the serialized data.
        """

        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "password"]

    def create(self, validated_data) -> CustomUser:
        """
        Create and return a new CustomUser instance, given the validated data.

        Ensures that the user's password is hashed before saving the user instance.

        :param validated_data: Creation data that has been validated by the serializer.
        :return: A new CustomUser instance.
        """
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance: CustomUser, validated_data) -> CustomUser:
        """
        Update and return an existing CustomUser instance, given the validated data.

        If a password is provided, it is hashed before saving the updated user instance.
        Otherwise, updates the instance with the provided data without changing the password.

        :param instance: The CustomUser instance to update.
        :param validated_data: Data containing the update data, validated by the serializer.
        :return: The updated CustomUser instance.
        """
        # Call the superclass method to handle updating fields other than the password
        user = super().update(instance, validated_data)
        # Check if 'password' is in validated_data to ensure it's intended to be updated
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
