from rest_framework import serializers
from .models import Book, Genre, Author
from rest_framework.serializers import SerializerMethodField


class BookSerializer(serializers.ModelSerializer):
    genre_name = SerializerMethodField()
    class Meta:
        model = Book
        fields = 'cover name author description\n' \
                 ' pages genre genre_name'.split()

    def get_genre_name(self, book):
        return book.genre_name

class AuthorSerializer(serializers.ModelSerializer):
    author_count = SerializerMethodField()
    class Meta:
        model = Author
        fields = 'name surname author_count'.split()

    def get_author_count(self, obj):
        return obj.books.all().count()


class GenresSerializer(serializers.ModelSerializer):
    genre_count = SerializerMethodField()
    # genre_count = BookSerializer()
    class Meta:
        model = Genre
        fields = 'name genre_count'.split()

    def get_genre_count(self, obj):
        return obj.books.all().count()
