from rest_framework import serializers
from .models import Books, Genres, Authors, Review, Favorite, SimilarGenre
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = 'id cover title summary pages author genre file genre_name author_name ' \
                 'created_date update_date rate'.split(' ')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
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
        fields = 'book user book_title'.split(' ')


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('book', )

    def create(self, validated_data):
        book = validated_data['book']
        user = self.context['request'].user
        favorite = Favorite.objects.create(user=user, book=book)
        return favorite


class ReadingBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingBookMark
        fields = '__all__'


class WillReadBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WillReadBookMark
        fields = '__all__'


class FinishBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishBookMark
        fields = '__all__'


class SimilarGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimilarGenre
        fields = '__all__'

