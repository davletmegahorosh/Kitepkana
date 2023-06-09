from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter
from .views import  TitleFilterAPIView, AuthorFilterAPIView, ReadingBookMarkAPIView, \
    WillReadBookMarkAPIView, FinishBookMarkAPIView, TitleSuggestView, \
    AuthorSuggestView
from .views import AuthorListView, AuthorDetailView, GenreListView, GenreDetailView
from .views import BookListView, BookDetailView, RecommendedBooks, AddStarRatingView, ReviewViewSet, \
    FavoriteListCreateView, FavoriteDeleteView, FinishBookMarkDeleteView, WillReadBookMarkDeleteView,\
    ReadingBookMarkDeleteView


router = routers.SimpleRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='authors-detail'),
    path('genres/', GenreListView.as_view(), name='genres-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genres-detail'),
    path('books/', BookListView.as_view(), name='books-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='books-detail'),
    path('recommended_books/', RecommendedBooks.as_view(), name='recommended_books'),
    path('add_star/', AddStarRatingView.as_view(), name='add_star'),

]

# Filters
urlpatterns += [
    path('titles_filter/', TitleFilterAPIView.as_view(), name='titles_filter'),
    path('authors_filter/', AuthorFilterAPIView.as_view(), name='authors_filter'),
    path('read_bookmark/', ReadingBookMarkAPIView.as_view(), name='read_bookmark'),
    path('read_bookmark/<int:pk>/', ReadingBookMarkDeleteView.as_view(), name='read_bookmark-detail'),
    path('will_read_bookmark/', WillReadBookMarkAPIView.as_view(), name='will_read_bookmark'),
    path('will_read_bookmark/<int:pk>/', WillReadBookMarkDeleteView.as_view(), name='will_read_bookmark-detail'),
    path('finish_bookmark/', FinishBookMarkAPIView.as_view(), name='finish_bookmark'),
    path('finish_bookmark/<int:pk>/', FinishBookMarkDeleteView.as_view(), name='finish-detail'),
    path('favorite/', FavoriteListCreateView.as_view(), name='favorite'),
    path('favorite/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite_detail'),
    path('title_suggest/', TitleSuggestView.as_view(), name='title_suggest'),
    path('author_suggest/', AuthorSuggestView.as_view(), name='author_suggest')

]
urlpatterns += router.urls
