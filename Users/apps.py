"""Users app configuration."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Users app default configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "Users"
