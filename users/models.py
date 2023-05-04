from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


<<<<<<< HEAD
class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    verification_code = models.CharField(max_length=8, verbose_name='Код для подтверждения')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
=======
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Введите действительный адрес электронной почты')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError('Superuser has to have is_staff being True')

        if extra_fields.get("is_superuser") is not True:
            raise ValueError('Superuser has to have superuser being True')

        return self.create_user(email=email, username=username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=275, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_username(self):
        return self.username

    def __str__(self):
        return self.email

>>>>>>> Dev
