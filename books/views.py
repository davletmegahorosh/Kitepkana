from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Books, Genres, Authors
from .serializers import BookSerializer, GenresSerializer, AuthorSerializer
from rest_framework import views
from rest_framework import permissions
from .permissions_book import IsAdminOrReadonly, IsOwnerOrReadOnly


""" Views for single objects. CRUD Management. These views for admin """


class AuthorCreateView(generics.CreateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer


class AuthorDeleteView(generics.DestroyAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer


class AuthorRetrieveView(generics.RetrieveAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer


class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer


class GenreCreateView(generics.CreateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class GenreRetrieveView(generics.RetrieveAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class GenreUpdateView(generics.UpdateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class GenreDeleteView(generics.DestroyAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(generics.UpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookDeleteView(generics.DestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


"""Views for users. These views return list objects of models"""


class AuthorListView(generics.ListAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer


class GenreListView(generics.ListAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class BookListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


"""Views detail for single object. This views show detail info for user or admin"""


class AuthorDetailApiView(views.APIView):
    def get(self, request, pk):
        data = get_object_or_404(Authors.objects.all(), id=pk)
        author = Books.objects.filter(author=data)
        serializer = BookSerializer(author, many=True).data
        return Response(data={f"Автор:  {data.name}": serializer}, status=status.HTTP_200_OK)


class GenreDetailApiView(views.APIView):
    def get(self, request, pk):
        data = get_object_or_404(Genres.objects.all(), id=pk)
        genre = Books.objects.filter(genre=data)
        serializer = BookSerializer(genre, many=True).data
        return Response(data={f"Жанр:  {data.genre_name}": serializer}, status=status.HTTP_200_OK)

