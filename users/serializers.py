from rest_framework import serializers



class UsersSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()