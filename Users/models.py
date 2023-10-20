from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    user_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
