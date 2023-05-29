from rest_framework import serializers
<<<<<<< HEAD
from .models import Books, Genres, Authors, Review, Favorite
=======
from .models import Book, Genre, Author
from rest_framework.exceptions import ValidationError
>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a


class BookSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = Books
        fields = 'id cover title summary pages author genre file genre_name author_name ' \
                 'created_date update_date rate'.split(' ')


=======
        model = Book
        fields = '__all__'

>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = 'id name surname'.split()

<<<<<<< HEAD

=======
>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a
class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

<<<<<<< HEAD

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = 'id get_user get_book review_text created user book'.split(' ')
=======
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
>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a

    class Meta:
        model = Genre
        fields = '__all__'

<<<<<<< HEAD
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = 'book user book_title'.split(' ')
=======
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
>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('book', )

    def create(self, validated_data):
        book = validated_data['book']
        user = self.context['request'].user
        favorite = Favorite.objects.create(user=user, book=book)
        return favorite
