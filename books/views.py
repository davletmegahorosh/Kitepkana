from django.db.models.functions import Round
from django.http import Http404, JsonResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from pypdf import PdfReader
from rest_framework import status, generics, mixins
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Books, Genres, Authors, Review, Favorite, Page
from .permissions_book import IsOwner
from .serializers import ReviewListSerializer, FavoriteCreateSerializer, \
    FavoriteSerializer, CreateRatingSerializer
from rest_framework import viewsets
from random import sample
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark
from .serializers import ReadingBookMarkSerializer, WillReadBookMarkSerializer, FinishBookMarkSerializer
from .service import get_client_username, parse_pdf, BookAPIPagination
from .serializers import AuthorListSerializer, AuthorDetailSerializer
from .serializers import GenreListSerializer, GenreDetailSerializer, BookListSerializer
from .serializers import BookDetailSerializer, FinishBookMarkCreateSerializer
from .serializers import WillReadBookMarkCreateSerializer, ReadingBookMarkCreateSerializer, ReviewCreateSerializer
from .serializers import ReviewListSerializer, SuggestSerializer, PageBookSerializer, GetFileFieldFromBookSerializer
from django.db import models
from Kitepkanaproject.settings import BASE_DIR


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
        total_rating_value = models.Avg(models.F('ratings__star__value'))
        res = Round(total_rating_value, precision=1)
        books = Books.objects.annotate(
            middle_star=res)
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
        total_rating_value = models.Avg(models.F('ratings__star__value'))
        res = Round(total_rating_value, precision=1)
        books = Books.objects.annotate(
            middle_star=res)

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
    serializer_class = ReviewListSerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update':
            return ReviewCreateSerializer
        if self.action == 'list':
            return ReviewListSerializer
        return ReviewListSerializer

    def get_permissions(self):

        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
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
    serializer_class = SuggestSerializer
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


# class GenreFilter(filters.FilterSet):
#     genres = CharFilterInFilter(field_name='genre_name', lookup_expr='in')
#
#     class Meta:
#         model = Genres
#         fields = ['genre_name']
#
#
# class GenreFilterAPIView(ListAPIView):
#     queryset = Genres.objects.all()
#     serializer_class = GenreDetailSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = GenreFilter


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
    serializer_class = BookDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_queryset(self):
        books = Books.objects.annotate(
            middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
        )

        return books


class AuthorFilter(filters.FilterSet):
    authors = CharFilterInFilter(field_name='author__fullname', lookup_expr='in')

    class Meta:
        model = Books
        fields = ['author']


class AuthorFilterAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = SuggestSerializer
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
class ReadingBookMarkAPIView(ListCreateAPIView, ):
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


# @extend_schema_view(
#     get=extend_schema(
#         summary='Фильтрация книг по жанрам',
#         description='Необходимо передать параметр в запрос: query=value\n'
#                     '\n Пример: http://localhost:8000/?query=Роман'))
# class GenreSuggestView(ListAPIView):
#     serializer_class = SuggestSerializer
#
#     def get_queryset(self):
#         query = self.request.query_params.get('query', '')
#         if query:
#             return Books.objects.filter(genre__genre_name__startswith=query)[:5]
#         return Books.objects.none()


class TitleSuggestView(ListAPIView):
    serializer_class = SuggestSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            return Books.objects.filter(title__startswith=query)[:5]
        return Books.objects.none()


class AuthorSuggestView(ListAPIView):
    serializer_class = SuggestSerializer

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
    ))
class AddStarRatingView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def post(self, request: Request):
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=get_client_username(request))
        return Response(status=status.HTTP_201_CREATED)


class MainPageView(APIView):
    author_list_serializer = AuthorListSerializer

    def get(self, request):
        serializer_context = {
            'request': request,
        }
        authors = Authors.objects.all()
        author_list_serializer = self.author_list_serializer(authors, many=True, context=serializer_context).data
        return Response(data={'author_list': author_list_serializer})


class ReadingBookView(generics.GenericAPIView):
    queryset = Page.objects.all()
    pagination_class = BookAPIPagination
    serializer_class = PageBookSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Books, id=self.kwargs.get('pk'))
        filtered_data = Page.objects.filter(book=book)
        end_pages = len(filtered_data)
        get_page = request.GET.get('page')
        current_page = get_page
        user = request.user
        if current_page is None:
            current_page = 1
        else:
            pass
        # checking page

        if int(current_page) >= 1 and int(current_page)< end_pages:
            print('start index')
            # Create ReadingBookmarkObject
            exist_obj = ReadingBookMark.objects.filter(user=user, book=book)
            if exist_obj:
                pass
            elif not exist_obj:
                finish = ReadingBookMark.objects.create(user=user, book=book)
                finish.save()

            # Create FinishBookmarkobject
        elif int(current_page) == end_pages:
            bookmark_reading = ReadingBookMark.objects.get(user=user, book=book)
            if bookmark_reading:
                bookmark_reading.delete()
            exist_obj = FinishBookMark.objects.filter(user=user, book=book)
            if exist_obj:
                pass
            elif not exist_obj:
                finish = FinishBookMark.objects.create(user=user, book=book)
                finish.save()

            print('end index')

        queryset = self.filter_queryset(filtered_data)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ForBookCreatePagesAPIView(generics.GenericAPIView):
    queryset = Page.objects.all()
    serializer_class = PageBookSerializer
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Books, id=self.kwargs.get('pk'))
        book_serializer = GetFileFieldFromBookSerializer(book, many=False).data
        filepath = f"{BASE_DIR}{book_serializer['file']}"
        reader = PdfReader(filepath)
        for page in reader.pages:
            text = page.extract_text()
            Page.objects.create(
                text=text,
                book=book
            )

        return Response(data='Page objects created')
