from django.db.models import Q
from django.http import Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from rest_framework import status, generics, mixins
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Books, Genres, Authors, Review, Favorite, SimilarGenre
from .permissions_book import IsOwner
from .serializers import BookSerializer, GenresSerializer, ReviewSerializer, FavoriteCreateSerializer, \
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
from .serializers import BookDetailSerializer, BookSimpleSerializer, FinishBookMarkCreateSerializer
from .serializers import WillReadBookMarkCreateSerializer, ReadingBookMarkCreateSerializer, ReviewCreateSerializer
from django.db import models


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения всех авторов'
    )
)
class AuthorListView(generics.GenericAPIView,
                     mixins.ListModelMixin):
    queryset = Authors.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения детальной информации об авторе',
        description='Требуется указать идентификатор автора'
    )
)
class AuthorDetailView(generics.GenericAPIView,
                       mixins.RetrieveModelMixin):
    queryset = Authors.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        summary='Метод для вывода списка жанров',

    )
)
class GenreListView(generics.GenericAPIView,
                    mixins.ListModelMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreListSerializer
    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения детальной информации о жанре',

    )
)
class GenreDetailView(generics.GenericAPIView,
                      mixins.RetrieveModelMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения списка книг'
    )
)
class BookListView(generics.GenericAPIView,
                   mixins.ListModelMixin):
    queryset = Books.objects.all()
    serializer_class = BookListSerializer
    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        books = Books.objects.annotate(
            middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
        )
        return books


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения детальной информации о книге',
        description='Требуется указать идентификатор книги'
    )
)
class BookDetailView(generics.GenericAPIView,
                     mixins.RetrieveModelMixin):
    queryset = Books.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        books = Books.objects.annotate(
            middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
        )

        return books


@extend_schema_view(
    list=extend_schema(
        summary='Метод для получения списка отзывов'
    ),
    retrieve=extend_schema(
        summary='Детальная информация об отзыве',
        description='Требуется указать идентификатор отзыва'),
    update=extend_schema(
        summary='Метод для изменение отзыва',
        description='Требуется указать идентификатор отзыва',
    ),
    destroy=extend_schema(
        summary='Метод для удаления отзыва',
        description='Требуется указать идентификатор отзыва',
    ),
    create=extend_schema(
        summary='Метод для создания отзыва',
        description='Требуется заполнить соответсвующее поля',
    ),
    partial_update=extend_schema(
        summary='Метод для частичного изменения отзыва',
        description='Требуется указать идентификатор отзыва',
    ),

)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_class(self):
        if self.action == 'create' or 'destroy':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy' or 'update' or 'partial_update':
            permission_classes = [IsOwner]
        elif self.action == 'retrieve':
            permission_classes = [IsOwner or IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения рекомендованных книг'
    ))
class RecommendedBooks(generics.ListAPIView):
    serializer_class = BookSimpleSerializer
    permission_classes = (AllowAny,)
    queryset = Books.objects.all()

    def get_queryset(self):
        all_books = Books.objects.all()
        choice = len(all_books) // 2
        recommended = sample(list(all_books), choice)
        return recommended


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения списка избранных книг'
    ),
    post=extend_schema(
        summary='Метод для добавления книг в избранное',
        description='Если вы хотите добавить, то вам нужно указать идентификатор книги'
    ),
)
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


@extend_schema_view(
    delete=extend_schema(
        summary='Метод удаления книги из избранных',
        description='Если вы хотите удалить, то вам нужно указать идентификатор  - id'

    ))
class FavoriteDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class GenreFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genre_name', lookup_expr='in')

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


@extend_schema_view(
    get=extend_schema(
        summary='Фильтр по названию книг',
        description='Необходимо передать параметр в запрос: query=value\n'
                    '\n Пример: http://localhost:8000/?title=И дольше века длится день',
    ))
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


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения списка книг из закладки "Читаю"',
    ),
    post=extend_schema(
        summary='Метод для добавления книг в закладку "Читаю"',
        description='Требуется указать только идентификатор книги'
    ),
)
class ReadingBookMarkAPIView(ListCreateAPIView,):
    queryset = ReadingBookMark.objects.all()
    serializer_class = ReadingBookMarkSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReadingBookMarkCreateSerializer
        return ReadingBookMarkSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise Http404
        return ReadingBookMark.objects.filter(user=user)
@extend_schema_view(
    delete=extend_schema(
        summary='Метод удаления книги из закладки "Читаю',
        description='Если вы хотите удалить, то вам нужно указать идентификатор  - id'

    ))
class ReadingBookMarkDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = ReadingBookMarkSerializer
    queryset = ReadingBookMark.objects.all()


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения списка книг из закладки "Буду читать"',
    ),
    post=extend_schema(
        summary='Метод для добавления книг в закладку "Буду читать"',
        description='Требуется указать только идентификатор книги'
    )
)
class WillReadBookMarkAPIView(generics.ListCreateAPIView):
    queryset = WillReadBookMark.objects.all()
    serializer_class = WillReadBookMarkSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WillReadBookMarkCreateSerializer
        return WillReadBookMarkSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise Http404
        return WillReadBookMark.objects.filter(user=user)


@extend_schema_view(
    delete=extend_schema(
        summary='Метод удаления книги из закладки "Буду читать',
        description='Если вы хотите удалить, то вам нужно указать идентификатор  - id'

    ))
class WillReadBookMarkDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = WillReadBookMarkSerializer
    queryset = WillReadBookMark.objects.all()


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения списка книг из закладки "Прочитано"',
    ),
    post=extend_schema(
        summary='Метод для добавления книг в закладку "Прочитано"',
        description='Требуется указать только идентификатор книги'
    ),
    delete=extend_schema(
        summary='Метод для удаления книги из закладки \"Прочитано\". Для удаления'
    )
)
class FinishBookMarkAPIView(ListCreateAPIView):
    queryset = FinishBookMark.objects.all()
    serializer_class = FinishBookMarkSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FinishBookMarkCreateSerializer
        return FinishBookMarkSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise Http404
        return FinishBookMark.objects.filter(user=user)


@extend_schema_view(
    delete=extend_schema(
        summary='Метод удаления книги из закладки "Прочитано',
        description='Если вы хотите удалить, то вам нужно указать идентификатор  - id'

    ))
class FinishBookMarkDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = FinishBookMarkSerializer
    queryset = FinishBookMark.objects.all()



@extend_schema_view(
    get=extend_schema(
        summary='Фильтрация по похожим жанрам',
        description='Необходимо передать параметр в запрос: genre_name=value\n'
                    '\n Пример: http://localhost:8000/?query=Роман',
        parameters=[
            OpenApiParameter(
                name='Фильтрация по жанрам',
                location=OpenApiParameter.QUERY,
                required=False,
                type=OpenApiTypes.OBJECT
            )
        ],
        examples=[
            OpenApiExample(
                'Пример',
                value={"genre_name": "Pоман"}
            )
        ]
    )
)
class SimilarGenreView(ListAPIView):
    queryset = SimilarGenre.objects.all()
    serializer_class = SimilarGenreSerializer


@extend_schema_view(
    get=extend_schema(
        summary='Фильтрация книг по жанрам',
        description='Необходимо передать параметр в запрос: query=value\n'
                    '\n Пример: http://localhost:8000/?query=Роман'))
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


@extend_schema_view(
    get=extend_schema(
        summary='Фильтрация по автору',
        description='Необходимо передать параметр в запрос: query=value\n'
                    '\n Пример: http://localhost:8000/?query=Чингиз Айтматов',
        parameters=[
            OpenApiParameter(
                name='Фильтрация по автору',
                location=OpenApiParameter.QUERY,
                required=False,
                type=OpenApiTypes.OBJECT
            )
        ],
        examples=[
            OpenApiExample(
                'Пример',
                value={"query": "Чингиз Айтматов"}
            )
        ]
    )
)
class AuthorSuggestView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            return Books.objects.filter(author__fullname__startswith=query)[:5]
        return Books.objects.none()


@extend_schema_view(
    post=extend_schema(
        summary='Добавление оценки книге',
        description='Минимальное значение: 1\n'
                    '\nМаксимальное значение: 5\n'
                    '\n В качестве значения ключа \"book\" пишется идентификатор книги [id]\n',
        responses=status.HTTP_201_CREATED,
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "star": {"type": "int"},
                    "book": {"type": "int"}, },
            },
        }

        ,
        parameters=[
            OpenApiParameter(
                name='some_new_parameter',
                location=OpenApiParameter.HEADER,
                description='some new parameter for update post',
                required=False,
                type=dict

            ),
        ]
    )

)
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
