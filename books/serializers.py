from rest_framework import serializers
from .models import Books, Genres, Authors
from rest_framework.exceptions import ValidationError


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'