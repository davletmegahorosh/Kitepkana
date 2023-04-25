from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book, Author, Genre
from .serializers import BookSerializer, AuthorSerializer, GenresSerializer, AuthorValidateSerializer, BooksValidateSerializer
from rest_framework.response import Response
from rest_framework import status

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
