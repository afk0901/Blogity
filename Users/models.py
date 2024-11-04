"""Custom User Model Module.

This module defines a custom user model that extends Django's built-in
AbstractUser model. It is designed to provide a flexible foundation for
user management by allowing for additional fields and methods to be
added to the user model.
"""

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().order_by("username")


class CustomUser(AbstractUser):
    """Custom user model that extends the default AbstractUser model.

    This model inherits from Django's AbstractUser, using its built-in fields and
    functionalities such as username, email, password, first_name, and last_name.

    By inheriting AbstractUser, it retains the core authentication and authorization
    features provided by Django but allows for future enhancements and flexibility in
    user management.
    """

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Ignoring the type for MyPy. It's very obvious what the type should be.
    # MyPy gets a bit confused because of the UserManager inheritance.
    objects = CustomUserManager()  # type: ignore
