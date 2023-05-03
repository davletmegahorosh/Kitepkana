from rest_framework import serializers
from .models import Books, Genres, Authors, Review
from rest_framework.exceptions import ValidationError


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = 'cover name author description pages genre get_rate'.split(' ')


class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Review
        fields = 'text' 'get_book'.split(' ')

