from rest_framework import serializers
from django.contrib.auth.models import User


class UsersSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()