from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from .models import Books, Genres, Authors, Review, Favorite, SimilarGenre, Rating
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = 'id cover title summary pages author genre file genre author_name'.split(' ')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'


class SimilarGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarGenre
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    genres = SimilarGenreSerializer(many=True)

    class Meta:
        model = Genres
        fields = ('genre_name', 'genres')


class GenreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('genre_name',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id get_user get_book text created_date updated_date user book'.split(' ')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'book',)

    def create(self, validated_data):
        book = validated_data['book']
        user = self.context['request'].user
        review = Review.objects.create(user=user, book=book)
        return review


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSimpleSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    middle_star = serializers.IntegerField()

    class Meta:
        model = Books
        fields = ('id', 'title', 'cover', 'summary', 'author_name', 'middle_star', 'pages', 'file',
                  'author', 'genre', 'reviews')


class BookListSerializer(serializers.HyperlinkedModelSerializer):
    middle_star = serializers.IntegerField()

    class Meta:
        model = Books
        fields = ("id", "title", "cover", "middle_star", "url")


class BookSimpleSerializer(BookListSerializer):
    class Meta:
        model = Books
        fields = ("id", "title", "cover", "url")


class GenreListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genres
        fields = ("id", "genre_name", "url",)


class AuthorListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Authors
        fields = ("id", "url", "fullname")


class GenreDetailSerializer(serializers.ModelSerializer):
    genre_books = BookSimpleSerializer(many=True)

    class Meta:
        model = Genres
        fields = ("id", "genre_name", "genre_books",)


class AuthorDetailSerializer(serializers.ModelSerializer):
    author_books = BookSimpleSerializer(many=True)

    class Meta:
        model = Authors
        fields = ("id", "fullname", "author_books")


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Simple example',
            value=1,
            request_only=True,
            response_only=False,
        ),
        OpenApiExample(
            'Single param example',
            value={"s": 1},
            request_only=True,
            response_only=False,

        ),
    ],
)
class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'book')

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            user=validated_data.get('user', None),
            book=validated_data.get('book', None),
            defaults={'star': validated_data.get('star')}

        )

        return rating


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = 'book user book_title'.split(' ')


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('book',)

    def create(self, validated_data):
        book = validated_data['book']
        user = self.context['request'].user
        favorite = Favorite.objects.create(user=user, book=book)
        return favorite


class ReadingBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingBookMark
        fields = '__all__'


class ReadingBookMarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingBookMark
        fields = ('book',)

    def create(self, validated_data):
        book = validated_data['book']
        user = self.context['request'].user
        reading = ReadingBookMark.objects.create(user=user, book=book)
        return reading


class WillReadBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WillReadBookMark
        fields = '__all__'


class WillReadBookMarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WillReadBookMark
        fields = ('book',)

    def create(self, validated_data):
        book = validated_data['book']
        user = self.context['request'].user
        will = WillReadBookMark.objects.create(user=user, book=book)
        return will


class FinishBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishBookMark
        fields = '__all__'


class FinishBookMarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishBookMark
        fields = ('book',)

    def create(self, validated_data):
        book = validated_data['book']
        user = self.context['request'].user
        finish = FinishBookMark.objects.create(user=user, book=book)
        return finish
