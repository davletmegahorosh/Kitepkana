from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile
from rest_framework import serializers


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = 'user_photo username first_name last_name gender'.split()

    def validate_first_name(self, value):
        if len(value.strip()) > 100:
            raise serializers.ValidationError('Имя не должно превышать больше 100 символов')
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError('Имя должно состоять только из букв')
        return value

    def validate_last_name(self, value):
        if len(value.strip()) > 100:
            raise serializers.ValidationError('Фамилия не должна превышать больше 100 символов')
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError('Фамилия должна состоять только из букв')
        return value