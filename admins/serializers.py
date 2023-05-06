from rest_framework import serializers
from books.models import Books, Genres, Authors
from rest_framework.exceptions import ValidationError


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class AuthorSerializer(serializers.Serializer):
    class Meta:
        model = Authors
        fields = '__all__'


class GenresSerializer(serializers.Serializer):
    class Meta:
        model = Genres
        fields = '__all__'


class AuthorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    surname = serializers.CharField(max_length=50)

    def validate_author(self, author_id):
        try:
            Authors.objects.get(id=author_id)
        except Authors.DoesNotExist:
            raise ValidationError('This author does not exists!')
        return author_id


class GenreValidateSerializer(serializers.Serializer):
    genre_name = serializers.CharField(max_length=50)


    def validate_genre(self, genre_id):
        try:
            Genres.objects.get(id=genre_id)
        except Genres.DoesNotExist:
            raise ValidationError('This genre does not exists!')
        return genre_id

class BooksValidateSerializer(serializers.ModelSerializer):
    cover = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    author = serializers.IntegerField()
    description = serializers.CharField(max_length=5000)
    pages = serializers.FloatField()
    genre = serializers.IntegerField()

    def validate_author(self, author_id):
        try:
            Authors.objects.get(id=author_id)
        except Authors.DoesNotExist:
            raise ValidationError('This author does not exists!')
        return author_id

    def validate_genre(self, genre_id):
        try:
            Genres.objects.get(id=genre_id)
        except Genres.DoesNotExist:
            raise ValidationError('This genre does not exists!')
        return genre_id

class AdminPanelSerializer(serializers.Serializer):
    books = serializers.PrimaryKeyRelatedField(queryset=Books.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genres.objects.all(), many=True)
    authors = serializers.PrimaryKeyRelatedField(queryset=Authors.objects.all(), many=True)
    class Meta:
        model = None
        fields = 'books authors genres'.split()