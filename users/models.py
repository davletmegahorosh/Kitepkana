from django.db import models


class Users(models.Model):
    email = models.TextField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=16)
    is_admin = models.BooleanField()