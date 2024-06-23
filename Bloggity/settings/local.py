from .base import *  # noqa

DEBUG = True

SECRET_KEY = "12345"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "Bloggity",
        "USER": "postgres",
        "PASSWORD": "12345",
        "HOST": "localhost",
        "PORT": 5432,
    }
}

STATIC_URL = "/static_files/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./dev-logs.log",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
