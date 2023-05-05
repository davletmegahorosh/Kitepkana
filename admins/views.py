from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from books.models import Books, Authors, Genres
from admins.serializers import BookSerializer, AuthorSerializer, GenresSerializer, AuthorValidateSerializer, BooksValidateSerializer, AdminPanelSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import AdminPanelModel


class AuthorApiView(ListCreateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            author = Authors.objects.all()
            serializer = AuthorSerializer(author, many=True)
            return Response(data=serializer.data)
        if request.method == 'POST':
            serializer = AuthorValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data=serializer.errors,
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            name = serializer.validated_data.get('name')
            surname = serializer.validated_data.get('surname')
            author = Authors.objects.create(name=name, surname=surname)
            author.save()


class GenreApiView(ListCreateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            genre = Genres.objects.all()
            serializer = GenresSerializer(genre, many=True)
            return Response(data=serializer.data)
        if request.method == 'POST':
            serializer = AuthorValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data=serializer.errors,
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            name = serializer.validated_data.get('name')
            surname = serializer.validated_data.get('surname')
            author = Authors.objects.create(name=name, surname=surname)
            author.save()


class CatalogApiView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            book = Books.objects.all()
            serializer = BookSerializer(book, many=True)
            return Response(data=serializer.data)
        elif request.method == 'POST':
            serializer = BooksValidateSerializer(data=request.data)
            if not serializer.is_valid():
                if not serializer.is_valid():
                    return Response(data=serializer.errors,
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
                cover = serializer.validated_data.get('cover')
                name = serializer.validated_data.get('name')
                author = serializer.validated_data.get('')
                description = serializer.validated_data.get('description')
                pages = serializer.validated_data.get('pages')
                genre = serializer.validated_data.get('genre')
                book = Authors.objects.create(name=name, cover=cover, author=author, description=description, pages=pages, genre=genre)
                book.save()

class AdminPanelView(ListAPIView):
    queryset = AdminPanelModel.objects.all()
    serializer_class = AdminPanelSerializer