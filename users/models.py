from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .service import generate_verify_code

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, user_photo=None,
                    first_name=None, last_name=None, gender=None, verify_code=None, **extra_fields):
        if not email:
            raise ValueError('Введите действительный адрес электронной почты')
        code = generate_verify_code()

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, verify_code=code, **extra_fields)

        user.set_password(password)
        user.save()

        '''Создание профиля'''
        profile = Profile.objects.create(user=user, user_photo=user_photo, username=username,
                                         first_name=first_name, last_name=last_name, gender=gender)
        profile.save()

        return user

    def create_superuser(self, email, username, password=None, user_photo=None,
                         first_name=None, last_name=None, gender=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError('Superuser has to have is_staff being True')

        if extra_fields.get("is_superuser") is not True:
            raise ValueError('Superuser has to have superuser being True')

        return self.create_user(email=email, username=username, password=password, user_photo=user_photo,
                                first_name=first_name, last_name=last_name, gender=gender, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=275, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=10)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_username(self):
        return self.username

    def __str__(self):
        return self.email


class Profile(models.Model):
    '''Профиль пользователя'''
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user_photo = models.ImageField(null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    gender = models.CharField(default="неизвестен", max_length=15, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.user_id and not self.username:
            self.username = self.user.username
        super().save(*args, **kwargs)




