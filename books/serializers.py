from rest_framework import serializers
from .models import Books, Genres, Authors, Review, Favorite


class BookSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Books
        fields = 'id cover title summary pages author genre file genre_name author_name ' \
                 'created_date update_date user rate'.split(' ')


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


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = 'id get_user get_book review_text created user book'.split(' ')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('book', )
    def create(self, validated_data):
        book = validated_data['book']
        user = self.context['request'].user
        favorite = Favorite.objects.create(user=user, book=book)
        return favorite