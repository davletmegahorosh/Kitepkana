from django.db.models import Q
from django.http import Http404
from rest_framework import status, generics, mixins
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Books, Genres, Authors, Review, Favorite, SimilarGenre
from .permissions_book import IsOwner
from .serializers import BookSerializer, GenresSerializer,ReviewSerializer, FavoriteCreateSerializer, \
    FavoriteSerializer, SimilarGenreSerializer, CreateRatingSerializer
from rest_framework import viewsets
from random import sample
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark
from .serializers import ReadingBookMarkSerializer, WillReadBookMarkSerializer, FinishBookMarkSerializer
from .service import get_client_username
from .serializers import AuthorListSerializer, AuthorDetailSerializer, GenreListSerializer
from .serializers import GenreListSerializer, GenreDetailSerializer, BookListSerializer
from .serializers import BookDetailSerializer, BookSimpleSerializer
from django.db import models


class AuthorListView(generics.GenericAPIView,
                     mixins.ListModelMixin):
    queryset = Authors.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = (AllowAny, )

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AuthorDetailView(generics.GenericAPIView,
                       mixins.RetrieveModelMixin):
    queryset = Authors.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GenreListView(generics.GenericAPIView,
                    mixins.ListModelMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreListSerializer
    permission_classes = (AllowAny, )

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GenreDetailView(generics.GenericAPIView,
                      mixins.RetrieveModelMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreDetailSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BookListView(generics.GenericAPIView,
                    mixins.ListModelMixin):
    queryset = Books.objects.all()
    serializer_class = BookListSerializer
    permission_classes = (AllowAny, )

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        books = Books.objects.annotate(
            middle_star=models.Sum(models.F('ratings__star__value'))/ models.Count(models.F('ratings'))
        )
        return books


class BookDetailView(generics.GenericAPIView,
                      mixins.RetrieveModelMixin):
    queryset = Books.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        books = Books.objects.annotate(
            middle_star = models.Sum(models.F('ratings__star__value'))/ models.Count(models.F('ratings'))
        )

        return books


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwner, )


class RecommendedBooks(generics.ListAPIView):
    serializer_class = BookSimpleSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        all_books = Books.objects.all()
        choice = len(all_books) // 2
        recommended = sample(list(all_books), choice)
        return recommended


class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FavoriteSerializer
        return FavoriteCreateSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise Http404
        return Favorite.objects.filter(user=user)


class FavoriteDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()




class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class GenreFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genre_name',  lookup_expr='in')


    class Meta:
        model = Genres
        fields = ['genre_name']


class GenreFilterAPIView(ListAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GenreFilter


class TitleFilter(filters.FilterSet):
    titles = CharFilterInFilter(field_name='title', lookup_expr='in')

    class Meta:
        model = Books
        fields = ['title']


class TitleFilterAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class AuthorFilter(filters.FilterSet):
    authors = CharFilterInFilter(field_name='author__name', lookup_expr='in')

    class Meta:
        model = Books
        fields = ['author']


class AuthorFilterAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter


class ReadingBookMarkAPIView(ListCreateAPIView):
    queryset = ReadingBookMark.objects.all()
    serializer_class = ReadingBookMarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WillReadBookMarkAPIView(ListCreateAPIView):
    queryset = WillReadBookMark.objects.all()
    serializer_class = WillReadBookMarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FinishBookMarkAPIView(ListCreateAPIView):
    queryset = FinishBookMark.objects.all()
    serializer_class = FinishBookMarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SimilarGenreView(ListAPIView):
    queryset = SimilarGenre.objects.all()
    serializer_class = SimilarGenreSerializer


class GenreSuggestView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            return Books.objects.filter(genre__genre_name__startswith=query)[:5]
        return Books.objects.none()


class TitleSuggestView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            return Books.objects.filter(title__startswith=query)[:5]
        return Books.objects.none()


class AuthorSuggestView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            return Books.objects.filter(author__name__startswith=query)[:5]
        return Books.objects.none()


class AddStarRatingView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def post(self, request: Request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=get_client_username(request))
        return Response(status=status.HTTP_201_CREATED)