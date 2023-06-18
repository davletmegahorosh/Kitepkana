from djoser.serializers import UserCreateSerializer, UserDeleteSerializer as DjoserUserDeleteSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .models import Profile
from rest_framework import serializers, exceptions
import users.constants
User = get_user_model()


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')


class UserDeleteSerializer(DjoserUserDeleteSerializer):
    def delete(self):
        user = self.context['request'].user
        user.delete()


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


class ForReviewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("username", "user_photo")


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # uid validation have to be here, because validate_<field_name>
        # doesn't work with modelserializer
        try:
            code = self.initial_data.get("code", "")
            self.user = User.objects.get(verify_code=code)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_code"
            raise ValidationError(
                {"code": [self.error_messages[key_error]]}, code=key_error
            )
        return code

class ActivationSerializer(CodeSerializer):
    default_error_messages = {
        "invalid_code": users.constants.Messages.VERIFY_CODE_ERROR
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_active:
            return attrs
        raise exceptions.PermissionDenied(self.error_messages["invalid_code"])
