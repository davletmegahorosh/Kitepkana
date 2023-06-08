from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import RatingStar
from .models import Books, Genres, Authors, Review, Favorite, Rating
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = 'id cover title summary pages author genre file genre author_name'.split(' ')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('genre_name',)


class GenreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('genre_name',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id get_user get_book text created_date updated_date user book'.split(' ')


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id get_user get_book text created_date updated_date'.split(' ')


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'book', 'text')

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            book = validated_data['book']
        except KeyError:
            raise ValidationError({"book":["This field is required."]})
        try:
            text = validated_data['text']
        except KeyError:
            raise ValidationError({"text":["This field is required."]})

        review = Review.objects.create(user=user, book=book, text=text)
        return review

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSimpleSerializer(many=True)
    reviews = ReviewListSerializer(many=True)
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
        user = validated_data.get('user', None)
        book = validated_data.get('book', None)
        bew = validated_data.get('star')
        star = RatingStar.objects.get(value=bew.id)
        # print(star.id)

        found = Rating.objects.filter(user=user, book=book)
        if found:
            rating_obj = found[0]
            rating_obj.user = user
            rating_obj.book = book
            rating_obj.star = star
            rating_obj.save()
            return rating_obj

        else:
            rating = Rating.objects.create(
                user=validated_data.get('user', None),
                book=validated_data.get('book', None),
                star=star

            )
            return rating


class FavoriteSerializer(serializers.ModelSerializer):
    book_cover = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = 'id book_title book_cover'.split(' ')

    def get_book_cover(self, favorite):
        obj = get_object_or_404(Books, pk=favorite.book.id)
        serializer = BookSerializer(obj, many=False).data
        book_cover = serializer['cover']
        return book_cover


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('book',)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            book = validated_data['book']
        except KeyError:
            raise ValidationError({"book":["This field is required."]})
        exist_obj = Favorite.objects.filter(user=user, book=book)
        if exist_obj:
            raise ValidationError("Данная книга уже имеется во вкладке 'Избранное'")
        favorite = Favorite.objects.create(user=user, book=book)
        return favorite


class ReadingBookMarkSerializer(serializers.ModelSerializer):
    book_cover = serializers.SerializerMethodField()

    class Meta:
        model = ReadingBookMark
        fields = ("id", "book_title", "book_cover")

    def get_book_cover(self, readingbookmark):
        obj = get_object_or_404(Books, pk=readingbookmark.book.id)
        serializer = BookSerializer(obj, many=False).data
        book_cover = serializer['cover']
        return book_cover


class ReadingBookMarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingBookMark
        fields = ('book',)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            book = validated_data['book']
        except KeyError:
            raise ValidationError({"book": ["This field is required."]})
        exist_obj = ReadingBookMark.objects.filter(user=user, book=book)
        if exist_obj:
            raise ValidationError("Данная книга уже имеется во вкладке 'Читаю' ")
        reading = ReadingBookMark.objects.create(user=user, book=book)
        return reading


class WillReadBookMarkSerializer(serializers.ModelSerializer):
    book_cover = serializers.SerializerMethodField()

    class Meta:
        model = WillReadBookMark
        fields = ("id", "book_title", "book_cover")

    def get_book_cover(self, willreadbookmark):
        obj = get_object_or_404(Books, pk=willreadbookmark.book.id)
        serializer = BookSerializer(obj, many=False).data
        book_cover = serializer['cover']
        return book_cover


class WillReadBookMarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WillReadBookMark
        fields = ('book',)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            book = validated_data['book']
        except KeyError:
            raise ValidationError({"book": ["This field is required."]})
        exist_obj = WillReadBookMark.objects.filter(user=user, book=book)
        if exist_obj:
            raise ValidationError("Данная книга уже имеется во вкладке 'Буду читать' ")
        will = WillReadBookMark.objects.create(user=user, book=book)
        return will


class FinishBookMarkSerializer(serializers.ModelSerializer):
    book_cover = serializers.SerializerMethodField()

    class Meta:
        model = FinishBookMark
        fields = ("id", "book_title", "book_cover",)

    def get_book_cover(self, finishbookmark):
        obj = get_object_or_404(Books, pk=finishbookmark.book.id)
        serializer = BookSerializer(obj, many=False).data
        book_cover = serializer['cover']
        return book_cover


class FinishBookMarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishBookMark
        fields = ('book',)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            book = validated_data['book']
        except KeyError:
            raise ValidationError({"book": ["This field is required."]})
        exist_obj = FinishBookMark.objects.filter(user=user, book=book)
        if exist_obj:
            raise ValidationError("Данная книга уже имеется во вкладке 'Прочитано' ")
        finish = FinishBookMark.objects.create(user=user, book=book)
        return finish
