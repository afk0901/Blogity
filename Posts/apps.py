"""Posts app configuration."""

from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Posts app default configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "Posts"
