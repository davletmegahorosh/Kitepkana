from django.db import models
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User, Profile
from .service import get_object_or_void
from users.serializers import ForReviewProfileSerializer
from .models import RatingStar, Page
from .models import Books, Genres, Authors, Review, Favorite, Rating
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark


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
        fields = ("id", "url", "image", "short_story", "awards", "works")

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
    profile = ForReviewProfileSerializer()
    user_stars = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = 'id text created_date updated_date profile user_stars'.split(' ')

    def get_user_stars(self, review):
        # filtered = Rating.objects.get(book=review.book, user=review.profile)
        rate = get_object_or_void(Rating, book=review.book, user=review.profile)
        data = RatingSerializer(rate).data
        stars = get_object_or_void(RatingStar, id=data['star'])
        serializer = StarsSerializer(stars).data
        return serializer


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'book', 'text')

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            book = validated_data['book']
        except KeyError:
            raise ValidationError({"book": ["This field is required."]})
        try:
            text = validated_data['text']
        except KeyError:
            raise ValidationError({"text": ["This field is required."]})

        profile = get_object_or_404(Profile, user=user)

        review = Review.objects.create(profile=profile, book=book, text=text)
        return review

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


####BOOK
class BookListSerializer(serializers.HyperlinkedModelSerializer):
    middle_star = serializers.FloatField()
    read_book_url = serializers.SerializerMethodField()
    stash_book_url = False

    class Meta:
        model = Books
        fields = ("id", "title", "cover", "author_name", "middle_star", "read_book_url", "url")

    def get_read_book_url(self, books):
        domain = self.context['request'].build_absolute_uri('/')[:-1]+'/'
        read_url = domain+'read/book/'+ str(books.id)+'/'
        return read_url

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.stash_book_url is True:
            data.pop('read_book_url')
        return data


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
    class Meta:
        model = Genres
        fields = ("id", "genre_name", "url",)


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
    class Meta:
        model = Page
        fields = ("text",)


class GetFileFieldFromBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("file",)
