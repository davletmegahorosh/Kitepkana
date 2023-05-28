from rest_framework.views import APIView
from rest_framework.response import Response
from kitepkana.books.models import Books
from kitepkana.books.serializers import BookSerializer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


class BookSearchHintsView(APIView):
    def get(self, request):
        search_term = request.GET.get('q', '')
        books = Books.objects.filter(title__icontains=search_term)[:10]

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class GenreFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genre__genre_name', lookup_expr='in')

    class Meta:
        model = Books
        fields = ['genre']


class GenreSearchAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GenreFilter


class TitleFilter(filters.FilterSet):
    titles = CharFilterInFilter(field_name='title', lookup_expr='in')

    class Meta:
        model = Books
        fields = ['title']


class TitleSearchAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class AuthorFilter(filters.FilterSet):
    authors = CharFilterInFilter(field_name='author__name', lookup_expr='in')

    class Meta:
        model = Books
        fields = ['author']


class AuthorSearchAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter

