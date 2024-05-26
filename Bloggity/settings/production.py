"""Production Django settings."""

from GoogleClouds.secrets_utils import GoogleCloudsSecretManager

from .base import *  # noqa

secretmanager = GoogleCloudsSecretManager()

DEBUG = False

SECRET_KEY = secretmanager.access_secret("DJANGO_SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": secretmanager.access_secret("DB_NAME"),
        "USER": secretmanager.access_secret("DB_USER"),
        "PASSWORD": secretmanager.access_secret("DB_PASS"),
        "HOST": secretmanager.access_secret("DB_HOST"),
        "PORT": secretmanager.access_secret("DB_PORT"),
    }
}

STATIC_URL = secretmanager.access_secret("STATIC_URL")

ALLOWED_HOSTS = ["localhost"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "./logs.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}
