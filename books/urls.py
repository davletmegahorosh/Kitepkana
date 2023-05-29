from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from .views import GenreFilterAPIView, TitleFilterAPIView, AuthorFilterAPIView, ReadingBookMarkAPIView, \
    WillReadBookMarkAPIView, FinishBookMarkAPIView, SimilarGenreView, GenreSuggestView, TitleSuggestView, \
    AuthorSuggestView

from .views import AuthorListView, AuthorDetailView, GenreListView, GenreDetailView
from .views import BookListView, BookDetailView, RecommendedBooks, AddStarRatingView, ReviewViewSet, \
    FavoriteListCreateView, FavoriteDeleteView

router = routers.SimpleRouter()
router.register(r'api/v1/reviews', ReviewViewSet)


urlpatterns = [
    path('api/v1/authors/', AuthorListView.as_view(), name='author-list'),
    path('api/v1/authors/<int:pk>/', AuthorDetailView.as_view(), name='authors-detail'),
    path('api/v1/genres/', GenreListView.as_view(), name='genres-list'),
    path('api/v1/genres/<int:pk>/', GenreDetailView.as_view(), name='genres-detail'),
    path('api/v1/books/', BookListView.as_view(), name='books-list'),
    path('api/v1/books/<int:pk>/', BookDetailView.as_view(), name='books-detail'),
    path('api/v1/recommended_books/', RecommendedBooks.as_view(), name='recommended_books'),
    path('api/v1/add_star/', AddStarRatingView.as_view(), name='add_star'),

]

# Filters
urlpatterns+= [
    path('api/v1/genres_filter/', GenreFilterAPIView.as_view(), name='genres_filter'),
    path('api/v1/authors_filter/', AuthorFilterAPIView.as_view(), name='authors_filter'),
    path('api/v1/titles_filter/', TitleFilterAPIView.as_view(), name='titles_filter'),
    path('api/v1/read_bookmark/', ReadingBookMarkAPIView.as_view(), name='read_bookmark'),
    path('api/v1/will_read_bookmark/', WillReadBookMarkAPIView.as_view(), name='will_read_bookmark'),
    path('api/v1/finish_bookmark/', FinishBookMarkAPIView.as_view(), name='finish_bookmark'),
    path('api/v1/favorite/', FavoriteListCreateView.as_view(), name='favorite'),
    path('api/v1/favorite/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite_detail'),
    path('api/v1/alike_genre/', SimilarGenreView.as_view(), name='alike_genre'),
    path('api/v1/genre_suggest/', GenreSuggestView.as_view(), name='genre_suggest'),
    path('api/v1/title_suggest/', TitleSuggestView.as_view(), name='title_suggest'),
    path('api/v1/author_suggest/', AuthorSuggestView.as_view(), name='author_suggest')

]
urlpatterns+=router.urls