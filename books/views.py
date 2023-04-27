from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book, Genre, Author
from .serializers import BookSerializer, GenresSerializer, AuthorSerializer

class CatalogApiView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CatalogDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CatalogGenreApiView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class CatalogAuthorApiView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
