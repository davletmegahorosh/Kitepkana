from rest_framework import serializers
from .models import Book, Genre, Author
from rest_framework.serializers import SerializerMethodField


class BookSerializer(serializers.ModelSerializer):
    genre_name = SerializerMethodField()
    class Meta:
        model = Book
        fields = 'cover name author description pages genre_name'.split()

    def get_genre_name(self, book):
        return book.genre_name

class AuthorSerializer(serializers.ModelSerializer):
    Books_count = SerializerMethodField()
    class Meta:
        model = Author
        fields = 'name surname Books_count'.split()

    def get_Books_count(self, obj):
        return obj.books.all().count()


class GenresSerializer(serializers.ModelSerializer):
    book_count = SerializerMethodField()
    class Meta:
        model = Genre
        fields = 'name book_count'.split()

    def get_book_count(self, obj):
        return obj.books.all().count()
