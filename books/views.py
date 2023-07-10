from django.db.models.functions import Round
from django.http import Http404
from pypdf import PdfReader
from rest_framework import status, generics, mixins
from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Books, Genres, Authors, Review, Favorite, Page, Rating
from .permissions_book import IsOwner
from .serializers import  FavoriteCreateSerializer, \
    FavoriteSerializer, CreateRatingSerializer
from rest_framework import viewsets
from random import sample
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark, Progress
from books.serializers import  WillReadBookMarkSerializer
from .service import get_client_username, BookAPIPagination, get_object_or_void
from .serializers import AuthorListSerializer, AuthorDetailSerializer
from .serializers import GenreListSerializer, GenreDetailSerializer, BookListSerializer
from .serializers import BookDetailSerializer, FinishBookMarkCreateSerializer
from .serializers import  ReadingBookMarkCreateSerializer, ReviewCreateSerializer
from .serializers import ReviewListSerializer, SuggestSerializer, PageBookSerializer, GetFileFieldFromBookSerializer
from django.db import models
from Kitepkanaproject.settings import BASE_DIR
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import BaseInFilter, CharFilter, FilterSet
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import redirect


class AuthorListView(generics.GenericAPIView,
                     mixins.ListModelMixin):
    queryset = Authors.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AuthorDetailView(generics.GenericAPIView,
                       mixins.RetrieveModelMixin):
    queryset = Authors.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GenreListView(generics.GenericAPIView,
                    mixins.ListModelMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreListSerializer
    permission_classes = (AllowAny,)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GenreDetailView(generics.GenericAPIView,
                      mixins.RetrieveModelMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance_rating = get_object_or_void(Rating, user=request.user, book=instance.book)
        print(instance_rating)
        rating_serializer = CreateRatingSerializer(instance_rating, data=request.data, partial=partial)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        rating_serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.perform_update(rating_serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        rating_instance = get_object_or_void(Rating, user=request.user, book=instance.book)
        self.perform_destroy(instance)
        self.perform_destroy(rating_instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class RecommendedBooks(generics.ListAPIView):
    serializer_class = BookListSerializer
    permission_classes = (AllowAny,)
    queryset = Books.objects.all()

    def get_queryset(self):
        total_rating_value = models.Avg(models.F('ratings__star__value'))
        res = Round(total_rating_value, precision=1)
        books = Books.objects.annotate(
            middle_star=res
        )
        choice = len(books) // 2
        recommended = sample(list(books), choice)
        return recommended

class FavoriteListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FavoriteCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response(data={"msg": "created"})

    def get(self, request):
        serializer_context = {'request': request}
        favorite_id  = Favorite.objects.filter(user=self.request.user).values('id')
        favorite_obj = Favorite.objects.filter(id__in=favorite_id).values('book_id')
        id_list = [item ['book_id'] for item in favorite_obj]
        total_rating_value = models.Avg(models.F('ratings__star__value'))
        average = Round(total_rating_value, precision=1)
        books = Books.objects.annotate(
            middle_star=average
        ).filter(id__in=id_list)

        serializer = BookListSerializer(books, many=True, context=serializer_context).data

        return Response(data=serializer, status=status.HTTP_200_OK)


class FavoriteDeleteView(APIView):
    permission_classes = (IsOwner, )

    def delete(self, request, pk):
        book_obj = get_object_or_void(Books, id=pk)
        favorite_obj = get_object_or_void(Favorite, book=book_obj.id, user=self.request.user)
        favorite_obj.delete()
        return Response(data={"msg": "deleted"}, status=status.HTTP_204_NO_CONTENT)


class CharFilterInFilter(BaseInFilter, CharFilter):
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


class TitleFilter(FilterSet):
    titles = CharFilterInFilter(field_name='title', lookup_expr='in')


    class Meta:
        model = Books
        fields = ['title']


class TitleFilterAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = (AllowAny,)


    def get_queryset(self):
        books = Books.objects.annotate(
            middle_star=models.Sum(models.F('ratings__star__value')) / models.Count(models.F('ratings'))
        )

        return books


class AuthorFilter(FilterSet):
    authors = CharFilterInFilter(field_name='author__fullname', lookup_expr='in')

    class Meta:
        model = Books
        fields = ['author']


class AuthorFilterAPIView(ListAPIView):
    queryset = Books.objects.all()
    serializer_class = SuggestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter
    permission_classes = (AllowAny,)



# class ReadingBookMarkAPIView(ListCreateAPIView, ):
#     queryset = ReadingBookMark.objects.all()
#     serializer_class = ReadingBookMarkCreateSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return ReadingBookMarkCreateSerializer
#         return ReadingBookMarkCreateSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_anonymous:
#             raise Http404
#         return ReadingBookMark.objects.filter(user=user)


class ReadingBookMarkDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = ReadingBookMarkCreateSerializer
    queryset = ReadingBookMark.objects.all()

#
# class WillReadBookMarkAPIView(generics.ListCreateAPIView):
#     queryset = WillReadBookMark.objects.all()
#     serializer_class = WillReadBookMarkSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return WillReadBookMarkCreateSerializer
#         return WillReadBookMarkSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_anonymous:
#             raise Http404
#         return WillReadBookMark.objects.filter(user=user)


class WillReadBookMarkDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = WillReadBookMarkSerializer
    queryset = WillReadBookMark.objects.all()


class FinishBookMarkDeleteView(generics.DestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = FinishBookMarkCreateSerializer
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
    permission_classes = (AllowAny,)


    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            return Books.objects.filter(title__startswith=query)[:5]
        return Books.objects.none()


class AuthorSuggestView(ListAPIView):
    serializer_class = SuggestSerializer
    permission_classes = (AllowAny,)


    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            return Books.objects.filter(author__fullname__startswith=query)[:5]
        return Books.objects.none()


class AddStarRatingView(APIView):
    permission_classes = (IsAuthenticated,)


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


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 5000



class ReadingBookView(generics.GenericAPIView):
    queryset = Page.objects.all()
    serializer_class = PageBookSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        book_id = self.kwargs['pk']
        return Page.objects.filter(book_id=book_id)

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        page_number = request.query_params.get('page')
        user = request.user

        book = get_object_or_404(Books, id=book_id)
        pages = Page.objects.filter(book=book)
        end_pages = len(pages)

        try:
            progress = Progress.objects.get(user=user, book=book)
            if progress.current_page:
                page = pages.filter(number=progress.current_page).first()
            else:
                page = None

            if page_number:
                page_number = int(page_number)
                if page_number >= 1 and page_number <= end_pages:
                    progress.current_page = page_number
                    progress.save()
                    page = pages.filter(number=page_number).first()
                else:
                    # Если указан недопустимый номер страницы, перенаправляем на текущую страницу
                    return redirect(f"/read/book/{book_id}/?page={progress.current_page}")

            if not user.is_anonymous:
                if int(progress.current_page) >= 1 and int(progress.current_page) < end_pages:
                    print('start index')
                    exist_reading_obj = ReadingBookMark.objects.filter(user=user, book=book).exists()
                    if not exist_reading_obj:
                        reading_obj = ReadingBookMark.objects.create(user=user, book=book)
                        reading_obj.save()
                elif int(progress.current_page) == end_pages:
                    exist_reading_obj = ReadingBookMark.objects.filter(user=user, book=book).exists()
                    if not exist_reading_obj:
                        reading_obj = ReadingBookMark.objects.create(user=user, book=book)
                        reading_obj.save()

                    exist_finish_obj = FinishBookMark.objects.filter(user=user, book=book).exists()
                    if not exist_finish_obj:
                        finish_obj = FinishBookMark.objects.create(user=user, book=book)
                        finish_obj.save()

                    reading_obj = ReadingBookMark.objects.filter(user=user, book=book).first()
                    if reading_obj:
                        reading_obj.delete()

                    print('end index')

        except Progress.DoesNotExist:
            progress = Progress.objects.create(user=user, book=book, current_page=1)
            progress.save()
            page = None

        queryset = self.paginate_queryset(pages)
        serializer = self.get_serializer(queryset, many=True)
        response = self.get_paginated_response(serializer.data)

        current_page = request.query_params.get('page')
        response.data['current_page'] = current_page

        return response




class ManasReadingView(generics.GenericAPIView):
    queryset = Page.objects.all()
    serializer_class = PageBookSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    # def get_queryset(self):
    #     book_id = self.kwargs['pk']
    #     return Page.objects.filter(book_id=book_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get(self, request, *args, **kwargs):
        # book_id = self.kwargs['pk']
        page_number = request.query_params.get('page')
        user = request.user

        book = get_object_or_404(Books, title='Манас')
        pages = Page.objects.filter(book=book)
        end_pages = len(pages)

        try:
            progress = Progress.objects.get(user=user, book=book)
            if progress.current_page:
                page = pages.filter(number=progress.current_page).first()
            else:
                page = None

            if page_number:
                page_number = int(page_number)
                if page_number >= 1 and page_number <= end_pages:
                    progress.current_page = page_number
                    progress.save()
                    page = pages.filter(number=page_number).first()
                else:
                    # Если указан недопустимый номер страницы, перенаправляем на текущую страницу
                    return redirect(f"/read/book/{book.title.replace(' ', '-')}/?page={progress.current_page}")

            if not user.is_anonymous:
                if int(progress.current_page) >= 1 and int(progress.current_page) < end_pages:
                    print('start index')
                    exist_reading_obj = ReadingBookMark.objects.filter(user=user, book=book).exists()
                    if not exist_reading_obj:
                        reading_obj = ReadingBookMark.objects.create(user=user, book=book)
                        reading_obj.save()
                elif int(progress.current_page) == end_pages:
                    exist_reading_obj = ReadingBookMark.objects.filter(user=user, book=book).exists()
                    if not exist_reading_obj:
                        reading_obj = ReadingBookMark.objects.create(user=user, book=book)
                        reading_obj.save()

                    exist_finish_obj = FinishBookMark.objects.filter(user=user, book=book).exists()
                    if not exist_finish_obj:
                        finish_obj = FinishBookMark.objects.create(user=user, book=book)
                        finish_obj.save()

                    reading_obj = ReadingBookMark.objects.filter(user=user, book=book).first()
                    if reading_obj:
                        reading_obj.delete()

                    print('end index')

        except Progress.DoesNotExist:
            progress = Progress.objects.create(user=user, book=book, current_page=1)
            progress.save()
            page = None

        queryset = self.paginate_queryset(pages)
        serializer = self.get_serializer(queryset, many=True)
        response = self.get_paginated_response(serializer.data)

        current_page = request.query_params.get('page')
        response.data['current_page'] = current_page

        return response



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


class BookSearchFilterAPIView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['title', 'author__fullname', 'genre__genre_name', ]
    ordering_fields = ['middle_star', 'created_date']
    filterset_fields = ['genre__genre_name']

    def get_queryset(self):
        total_rating_value = models.Avg(models.F('ratings__star__value'))
        res = Round(total_rating_value, precision=1)
        books = Books.objects.annotate(
            middle_star=res)
        return books
