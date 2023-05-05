from rest_framework import serializers
from .models import Books, Genres, Authors


class BookSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Books
        fields = 'cover title summary pages author genre file genre_name author_name ' \
                 'created_date update_date user'.split(' ')


class AuthorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Authors
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Genres
        fields = '__all__'




