<<<<<<< HEAD
from django.db.models import Q
from django.http import Http404
=======
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book, Author, Genre
from .serializers import BookSerializer, AuthorSerializer, GenresSerializer, AuthorValidateSerializer, BooksValidateSerializer
from rest_framework.response import Response
>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import Books, Genres, Authors, Review, Favorite
from .serializers import BookSerializer, GenresSerializer, AuthorSerializer, ReviewSerializer, FavoriteCreateSerializer, \
    FavoriteSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from random import sample

<<<<<<< HEAD
""" Views for single objects. CRUD Management. These views for admin """


class BaseViewSet(CreateModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  GenericViewSet,
                  viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'update' \
                or self.action == 'create' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        pass


class AuthorViewSet(BaseViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer

    def retrieve(self, request, pk=None):
        author = get_object_or_404(Authors.objects.all(), id=pk)
        books = Books.objects.filter(author=author)
        serializer_autor = AuthorSerializer(author).data
        serializer_books = BookSerializer(books, many=True).data
        data = {"Автор": serializer_autor, "книги": serializer_books}
        return Response(data=data,
                        status=status.HTTP_200_OK)


class GenreViewSet(BaseViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

    def retrieve(self, request, pk=None):
        genre = get_object_or_404(Genres.objects.all(), id=pk)
        books = Books.objects.filter(genre=genre)
        serializer_genre = GenresSerializer(genre).data
        serializer_books = BookSerializer(books, many=True).data
        data = {"Жанр": serializer_genre, "Книги": serializer_books}
        return Response(data=data,
                        status=status.HTTP_200_OK)


class BookViewSet(BaseViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, pk=None):
        book = get_object_or_404(Books.objects.all(), id=pk)
        reviews = Review.objects.filter(book=book)
        serializer_book = BookSerializer(book).data
        serializer_reviews = ReviewSerializer(reviews, many=True).data
        data = {'Книга': serializer_book, "Отзывы": serializer_reviews}
        return Response(data=data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def recommended_books(self, request):
        all_books = Books.objects.all()
        recommended = sample(list(all_books), 3)
        serializer = BookSerializer(recommended, many=True)
        return Response(data=serializer.data)


class ReviewViewSet(BaseViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):

        if self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy' or self.action == 'update' \
                or self.action == 'partial_update':
            permission_classes = [IsAdminUser]

        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        review = get_object_or_404(Review.objects.all(), id=pk)
        serializer_review = ReviewSerializer(review).data
        return Response(data=serializer_review,
                        status=status.HTTP_200_OK)


"""Search Function"""


@api_view(['GET'])
def search(request):
    search_query = request.GET.get('q', '')  # Ключ должен называться q
    if search_query:
        books = Books.objects.filter(Q(title__icontains=search_query))
        if books:
            serializer = BookSerializer(books, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        author = get_object_or_404(Authors, name=search_query)
        books = Books.objects.filter(author=author.id)
        serializer = BookSerializer(books, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(data='Not Found', status=status.HTTP_404_NOT_FOUND)


class FavoriteViewSet(viewsets.GenericViewSet,
                      CreateModelMixin,
                      ListModelMixin):
    serializer_class = FavoriteCreateSerializer
    queryset = Favorite.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = Favorite.objects.filter(user=request.user.id)
        if queryset:
            serializer = FavoriteSerializer(queryset, many=True)
            return Response(data=serializer.data)
        raise Http404

=======
class AuthorApiView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            return Response(data=serializer.data)
        if request.method == 'POST':
            serializer = AuthorValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data=serializer.errors,
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            name = serializer.validated_data.get('name')
            surname = serializer.validated_data.get('surname')
            authors = Author.objects.create(name=name, surname=surname)
            authors.save()
            return Response(data={'message': 'Data received!',
                           'authors': AuthorSerializer(authors).data},
                     status=status.HTTP_201_CREATED)

class GenreApiView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            genre = Genre.objects.all()
            serializer = GenresSerializer(genre, many=True)
            return Response(data=serializer.data)
        if request.method == 'POST':
            serializer =GenresSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data=serializer.errors,
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            genre_name = serializer.validated_data.get('genre_name')
            genre = Genre.objects.create(genre_name=genre_name,)
            genre.save()

            return Response(data={'message': 'Data received!',
                           'genre': GenresSerializer(genre).data},
                     status=status.HTTP_201_CREATED)


class CatalogApiView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(data=serializer.data)
        if request.method == 'POST':
            serializer = BooksValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data=serializer.errors,
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            name = serializer.validated_data.get('name')
            cover = serializer.validated_data.get('cover')
            author = serializer.validated_data.get('author')
            description = serializer.validated_data.get('description')
            pages = serializer.validated_data.get('pages')
            genre = serializer.validated_data.get('genre')
            books = Book.objects.create(name=name, cover=cover, author=author, description=description,
                                          pages=pages, genre=genre)
            return Response(data={'message': 'Data received!',
                                  'books': BookSerializer(books).data},
                            status=status.HTTP_201_CREATED)



class CatalogDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a
