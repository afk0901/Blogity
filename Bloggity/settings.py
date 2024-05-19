"""Django settings for Bloggity project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

from GoogleClouds.secrets_utils import GoogleCloudsSecretManager

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

secretmanager = GoogleCloudsSecretManager()

DEBUG = bool(secretmanager.access_secret("DEBUG"))

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Users",
    "Posts",
    "rest_framework",
    "django_filters",
    "drf_spectacular",
]


SECRET_KEY = secretmanager.access_secret("DJANGO_SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

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

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Bloggity.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Bloggity.wsgi.application"

AUTH_USER_MODEL = "Users.CustomUser"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = secretmanager.access_secret("STATIC_URL")

# example.com, example2.com so on in the .env file
ALLOWED_HOSTS = secretmanager.access_secret("ALLOWED_HOSTS").split(",")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=99999),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=10),
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "REST API for posts and comments",
    "DESCRIPTION": """
    This API provides a comprehensive platform for managing user-generated content.
    Tailored for applications that involve creation, update,
    and deletion of posts and comments.

    Note: Everybody can see the posts and comments without any authentication.
    So feel free to execute a GET request on the endpoints below.

    To perform actions such as creation, update, and deletion,
    please follow these steps:

    1. User Registration: Create a user by sending a POST request to the
                          api/users endpoint.

    2. Authentication: Obtain your JWT authentication token by submitting your
                        username and password in a POST request to api/token/.

    3. Explore Endpoints: With your token, you can now use the PUT, POST,
                          and DELETE methods on the endpoints below to manage content.

    For more detailed guides and comprehensive information,
    please refer to our documentation on GitHub!
    """,
}
