from django.db import models
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
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
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserDeleteSerializer(DjoserUserDeleteSerializer):
    def delete(self):
        user = self.context['request'].user
        user.delete()


# class ProfileCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = 'user_photo username'.split()
#
#     def validate_first_name(self, value):
#         if len(value.strip()) > 100:
#             raise serializers.ValidationError('Имя не должно превышать больше 100 символов')
#         if not value.replace(' ', '').isalpha():
#             raise serializers.ValidationError('Имя должно состоять только из букв')
#         return value
#
#     def validate_last_name(self, value):
#         if len(value.strip()) > 100:
#             raise serializers.ValidationError('Фамилия не должна превышать больше 100 символов')
#         if not value.replace(' ', '').isalpha():
#             raise serializers.ValidationError('Фамилия должна состоять только из букв')
#         return value


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    reading = serializers.SerializerMethodField()
    finish = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("user_photo", "username", "email", "password", "reading", "finish")

    def get_email(self, profile):
        user = get_object_or_404(User, email=profile.user)
        return user.email

    def get_password(self, profile):
        user = get_object_or_404(User, email=profile.user)
        return user.stash

    def get_reading(self, profile):
        from books.serializers import ReadingBookMarkCreateSerializer, BookSerializer
        from books.models import ReadingBookMark, Books
        filter_bookmark = ReadingBookMark.objects.filter(user=profile.user)
        serializer = ReadingBookMarkCreateSerializer(filter_bookmark, many=True).data
        book_id_list = [item['book'] for item in serializer]
        total_rating_value = models.Avg(models.F('ratings__star__value'))
        average = Round(total_rating_value, precision=1)
        queryset = Books.objects.annotate(
            middle_star=average
        ).filter(id__in=book_id_list)
        books_serializer = BookSerializer(queryset, many=True).data
        return books_serializer

    def get_finish(self, profile):
        from books.serializers import FinishBookMarkCreateSerializer, BookSerializer
        from books.models import FinishBookMark,Books
        filter_bookmark = FinishBookMark.objects.filter(user=profile.user)
        serializer = FinishBookMarkCreateSerializer(filter_bookmark, many=True).data
        book_id_list = [item['book'] for item in serializer]
        total_rating_value = models.Avg(models.F('ratings__star__value'))
        average = Round(total_rating_value, precision=1)
        queryset = Books.objects.annotate(
            middle_star=average
        ).filter(id__in=book_id_list)
        books_serializer = BookSerializer(queryset, many=True).data
        return books_serializer


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
