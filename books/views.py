from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Books, Genres, Authors
from .serializers import BookSerializer, GenreValidateSerializer, GenresSerializer, BooksValidateSerializer, \
    AuthorValidateSerializer, AuthorSerializer


class AuthorApiView(ListCreateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        author = Authors.objects.all()
        serializer = AuthorSerializer(author, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AuthorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = Authors.objects.create(**serializer.validated_data)
        author.save()
        return Response(data={'Author Created'}, status=status.HTTP_200_OK)


class GenreApiView(ListCreateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

    def get(self, request, *args, **kwargs):
        genre = Genres.objects.all()
        serializer = GenresSerializer(genre, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = GenreValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        genre = Genres.objects.create(**serializer.validated_data)
        genre.save()
        return Response(data={'Genre Created'}, status=status.HTTP_200_OK)


class BookApiView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        book = Books.objects.all()
        serializer = BookSerializer(book, many=True).data
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BooksValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = Books.object.create(**serializer.validated_data)
        book.save()
        return Response(data={'Book Created'}, status=status.HTTP_200_OK)


class CatalogApiView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class CatalogDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer