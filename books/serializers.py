from rest_framework import serializers
from .models import Book, Genre, Author
from rest_framework.exceptions import ValidationError


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = 'id name surname'.split()

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorValidateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    surname = serializers.CharField(max_length=50)

    class Meta:
        model = Author
        fields = '__all__'

    def validate_author(self, author_pk):
        try:
            Author.objects.get(id=author_pk)
        except Author.DoesNotExist:
            raise ValidationError('This author does not exists!')
        return author_pk

class GenreValidateSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(max_length=50)

    class Meta:
        model = Genre
        fields = '__all__'

    def validate_genre(self, genre_pk):
        try:
            Genre.objects.get(id=genre_pk)
        except Genre.DoesNotExist:
            raise ValidationError('This genre does not exists!')
        return genre_pk

class BooksValidateSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(allow_null=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=5000)
    pages = serializers.FloatField()

    class Meta:
        model = Book
        fields = '__all__'

    def validate_author(self, author_name):
        try:
            Author.objects.get(name=author_name)
        except Author.DoesNotExist:
            raise ValidationError('This author does not exists!')
        return author_name

    def validate_genre(self, genre_name):
        try:
            Genre.objects.get(genre_name=genre_name)
        except Genre.DoesNotExist:
            raise ValidationError('This genre does not exists!')
        return genre_name


