from rest_framework import serializers
from books.models import Books, Genres, Authors


class ForAdminBookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Books
        fields = ("id", "title", "url")


class ForAdminAuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Authors
        fields = ("id", "fullname", "url")


class ForAdminGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genres
        fields = ("id", "genre_name", "url")


class AdminPanelSerializer(serializers.Serializer):
    books = ForAdminBookSerializer(many=True)
    genres = ForAdminGenreSerializer(many=True)
    authors = ForAdminAuthorSerializer(many=True)

    class Meta:
        model = None
        fields = ('books', 'authors', 'genres')
