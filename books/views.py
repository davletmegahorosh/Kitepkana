from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Books, Genres, Authors
from .serializers import BookSerializer, GenresSerializer, AuthorSerializer
from rest_framework import views
"""Views for create objects"""


class AuthorCreateView(generics.CreateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer


class GenreCreateView(generics.CreateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


""" Views for single objects. CRUD Management. These views for admin """


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
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
#
#
#
