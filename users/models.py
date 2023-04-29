from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    verification_code = models.CharField(max_length=8, verbose_name='Код для подтверждения')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
