from django.db.models import Q
from rest_framework import generics, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Books, Genres, Authors
from .serializers import BookSerializer, GenresSerializer, AuthorSerializer
from rest_framework import views
from rest_framework import permissions
from .permissions_book import IsAdminOrReadonly, IsOwnerOrReadOnly
from rest_framework.decorators import api_view

""" Views for single objects. CRUD Management. These views for admin """


class AuthorCreateView(generics.CreateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = (permissions.IsAdminUser,)


class AuthorDeleteView(generics.DestroyAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = (permissions.IsAdminUser,)


class AuthorRetrieveView(generics.RetrieveAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = (IsAdminOrReadonly,)


class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = (permissions.IsAdminUser,)


class GenreCreateView(generics.CreateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    # permission_classes = (permissions.IsAdminUser,)


class GenreRetrieveView(generics.RetrieveAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    # permission_classes = (IsAdminOrReadonly,)


class GenreUpdateView(generics.UpdateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    # permission_classes = (permissions.IsAdminUser,)


class GenreDeleteView(generics.DestroyAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (permissions.IsAdminUser,)


class BookCreateView(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (permissions.IsAdminUser,)


class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (IsAdminOrReadonly,)


class BookUpdateView(generics.UpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (permissions.IsAdminUser,)


class BookDeleteView(generics.DestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (permissions.IsAdminUser,)


"""Views for users. These views return list objects of models"""


class AuthorListView(generics.ListAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.AllowAny,)


class GenreListView(generics.ListAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (permissions.AllowAny,)


class BookListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.AllowAny,)


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
