from django.db import models
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User, Profile
from .service import get_object_or_void, validate_star
from users.serializers import ForReviewProfileSerializer
from .models import RatingStar, Page
from .models import Books, Genres, Authors, Review, Favorite, Rating
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark
import string


class StarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingStar
        fields = ("value",)


class BookSerializer(serializers.HyperlinkedModelSerializer):
    middle_star = serializers.FloatField()

    class Meta:
        model = Books
        fields = 'id cover title summary author_name middle_star'.split(' ')


###AUTHOR
class BookTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = 'id title'.split(' ')


class AuthorListSerializer(serializers.HyperlinkedModelSerializer):
    works = serializers.SerializerMethodField()

    class Meta:
        model = Authors
        fields = ("id", "url", "image","fullname", "date_of_birth", "short_story", "awards", "works")

    def get_works(self, id):
        books = Books.objects.filter(author=id)
        serializer = BookTitleSerializer(books, many=True).data
        return serializer


##Author

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('genre_name',)


class GenreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('id', 'genre_name',)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("star",)


# Review
class ReviewListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_photo = serializers.SerializerMethodField()
    user_stars = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = 'id username user_photo user_stars text created_date updated_date'.split(' ')

    def get_user_stars(self, review):
        # filtered = Rating.objects.get(book=review.book, user=review.profile)
        rate = get_object_or_void(Rating, book=review.book, user=review.profile.user)
        data = RatingSerializer(rate).data
        stars = get_object_or_void(RatingStar, id=data['star'])
        serializer = StarsSerializer(stars).data
        return serializer['value']

    def get_username(self, review):
        profile = get_object_or_void(Profile, id=review.profile.id)
        serializer = ForReviewProfileSerializer(profile, many=False).data
        return serializer['username']

    def get_user_photo(self, review):
        profile = get_object_or_void(Profile, id=review.profile.id)
        serializer = ForReviewProfileSerializer(profile, many=False).data
        photo = self.context['request'].build_absolute_uri()[:-9]+serializer['user_photo']
        return photo


from django.core.exceptions import ObjectDoesNotExist

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'book', 'text')

    def create(self, validated_data):
        user = self.context['request'].user

        # Check if the user has already left 3 reviews
        if Review.objects.filter(profile__user=user).count() > 3:
            raise ValidationError('Вы можете оставить только до трех отзывов.')

        try:
            book = validated_data['book']
        except KeyError:
            raise ValidationError({"book": ["This field is required."]})

        try:
            text = validated_data['text']
        except KeyError:
            raise ValidationError({"text": ["This field is required."]})

        try:
            star = self.context['request'].data['star']
        except KeyError:
            raise ValidationError({"star": ["This field is required."]})

        # Check if the user has already left 3 star ratings
        if Rating.objects.filter(user=user).count() > 3:
            raise ValidationError('Вы можете установить только до трех рейтингов звезд.')

        try:
            star = RatingStar.objects.get(value=validate_star(star))
        except ObjectDoesNotExist:
            raise ValidationError({"star": ["Недопустимое значение рейтинга звезд."]})

        profile = get_object_or_404(Profile, user=user)

        if Rating.objects.filter(user=user, book=book).count() >= 3 and \
                Review.objects.filter(profile__user=user, book=book).count() >= 3:
            raise ValidationError('Вы уже оставили рейтинг для этой книги.')

        review = Review.objects.create(profile=profile, book=book, text=text)
        Rating.objects.create(user=user, book=book, star=star)

        return review

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


####BOOK
class BookListSerializer(serializers.HyperlinkedModelSerializer):
    middle_star = serializers.FloatField()

    class Meta:
        model = Books
        fields = ("id", "title", "cover", "author_name", "summary", "middle_star")


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSimpleSerializer(many=True)
    reviews = ReviewListSerializer(many=True)
    middle_star = serializers.FloatField()
    similar_books = serializers.SerializerMethodField()

    class Meta:
        model = Books
        fields = ('id', 'cover', 'title', 'author_name', 'publication_year', 'genre', 'middle_star',  'summary',
                  'reviews', 'similar_books')

    def get_similar_books(self, books):
        filter_genre = GenreSimpleSerializer(books.genre, many=True).data
        genres_id = [key['id'] for key in filter_genre]
        genres = Genres.objects.filter(id__in=genres_id)
        total_rating_value = models.Avg(models.F('ratings__star__value'))
        average = Round(total_rating_value, precision=1)
        queryset = Books.objects.annotate(
            middle_star=average
        ).filter(genre__in=genres).distinct()
        serializer_context = {'request': self.context['request']}
        response = BookListSerializer(queryset, many=True, context=serializer_context).data
        return response


###Book

class BookSimpleSerializer(BookListSerializer):
    class Meta:
        model = Books
        fields = ("id", "title", "cover", "url")


class SuggestSerializer(BookSimpleSerializer):
    class Meta:
        model = Books
        fields = ("id", "title", "cover", "author_name", "url")


class GenreListSerializer(serializers.HyperlinkedModelSerializer):
    extra_name = serializers.SerializerMethodField()

    class Meta:
        model = Genres
        fields = ("id", "genre_name", "extra_name")

    def get_extra_name(self, genres):
        return genres.genre_name


class GenreDetailSerializer(serializers.ModelSerializer):
    genre_books = BookSimpleSerializer(many=True)

    class Meta:
        model = Genres
        fields = ("id", "genre_name", "genre_books",)


class AuthorDetailSerializer(serializers.ModelSerializer):
    author_books = serializers.SerializerMethodField()

    class Meta:
        model = Authors
        fields = (
            "id", "image", "fullname", "date_of_birth", "place_of_birth", "citizenship","language", "genre", "bio",
            "literary_activity",
            "author_books",)

    def get_author_books(self, authors):
        total_rating_value = models.Avg(models.F('ratings__star__value'))

        average = Round(total_rating_value, precision=1)
        queryset = Books.objects.annotate(
            middle_star=average
        ).filter(author=authors).distinct()
        serializer_context = {'request': self.context['request']}
        serializer = BookListSerializer(queryset, many=True, context=serializer_context).data
        return serializer


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'book')

    def update(self, instance, validated_data):
        star_object = validated_data.get('star')
        id_star_object = get_object_or_void(RatingStar, value=star_object.id)
        instance.star = id_star_object
        instance.save()
        return instance

class FavoriteSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = 'id book'.split(' ')

    def get_book(self, favorite):
        serializer_context = {'request': self.context['request']}

        total_rating_value = models.Avg(models.F('ratings__star__value'))
        average = Round(total_rating_value, precision=1)
        queryset = Books.objects.annotate(
            middle_star=average,
        ).get(id=favorite.book.id)
        books_serializer = BookSerializer(queryset,context=serializer_context).data
        return books_serializer


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('book',)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            book = validated_data['book']
        except KeyError:
            raise ValidationError({"book": ["This field is required."]})
        exist_obj = Favorite.objects.filter(user=user, book=book)
        if exist_obj:
            raise ValidationError("Данная книга уже имеется во вкладке 'Избранное'")
        favorite = Favorite.objects.create(user=user, book=book)
        return favorite


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


class PageBookSerializer(serializers.ModelSerializer):
    current_page = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ('id', 'text', 'current_page')

    def get_current_page(self, obj):
        request = self.context.get('request')
        if request:
            return request.query_params.get('page')
        return None



class GetFileFieldFromBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("file",)
