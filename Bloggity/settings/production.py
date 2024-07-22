"""Production Django settings."""

from GoogleClouds.secrets_utils import GoogleCloudsSecretManager

from .base import *  # noqa

secretmanager = GoogleCloudsSecretManager()

DEBUG = False

SECRET_KEY = secretmanager.access_secret("DJANGO_SECRET_KEY")

INSTALLED_APPS += ["sslserver"]  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": secretmanager.access_secret("DB_NAME"),
        "USER": secretmanager.access_secret("DB_USER"),
        "PASSWORD": secretmanager.access_secret("DB_PASS"),
        "HOST": secretmanager.access_secret("DB_HOST"),
        "PORT": secretmanager.access_secret("DB_PORT"),
        "CONN_MAX_AGE": 300,
    }
}

STATIC_URL = "static_files/"

STATIC_ROOT = "Bloggity/static_files/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "./production-logs.log",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

CORS_ALLOWED_ORIGINS = ["https://arnarfreyr.is"]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
]

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_PRELOAD = True
