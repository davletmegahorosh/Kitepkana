from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter
from .views import TitleFilterAPIView, AuthorFilterAPIView,  TitleSuggestView, \
    AuthorSuggestView, ReadingBookView
from .views import AuthorListView, AuthorDetailView, GenreListView, GenreDetailView
from .views import BookListView, BookDetailView, RecommendedBooks, AddStarRatingView, ReviewViewSet, \
    FavoriteListCreateView, FavoriteDeleteView, FinishBookMarkDeleteView, WillReadBookMarkDeleteView,\
    ReadingBookMarkDeleteView, ForBookCreatePagesAPIView,  BookSearchFilterAPIView, ManasReadingView
from .views import MainPageView

router = routers.SimpleRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('search_filter/', BookSearchFilterAPIView.as_view()),
    path('create_page_book/<int:pk>/', ForBookCreatePagesAPIView.as_view()),
    path('read/book/<int:pk>/', ReadingBookView.as_view(), name='read_book'),
    path('read/book/manas/', ManasReadingView.as_view()),
    path('main/', MainPageView.as_view(), name='authors-detail'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='authors-detail'),
    path('genres/', GenreListView.as_view(), name='genres-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genres-detail'),
    path('books/', BookListView.as_view(), name='books-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='books-detail'),
    path('recommended_books/', RecommendedBooks.as_view(), name='recommended_books'),
]

# Filters
urlpatterns += [
    path('favorite/', FavoriteListCreateView.as_view(), name='favorite'),
    path('titles_filter/', TitleFilterAPIView.as_view(), name='titles_filter'),
    path('authors_filter/', AuthorFilterAPIView.as_view(), name='authors_filter'),
    path('read_bookmark/<int:pk>/', ReadingBookMarkDeleteView.as_view(), name='read_bookmark-detail'),
    path('finish_bookmark/<int:pk>/', FinishBookMarkDeleteView.as_view(), name='finish-detail'),
    path('favorite/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite_detail'),
    path('title_suggest/', TitleSuggestView.as_view(), name='title_suggest'),
    path('author_suggest/', AuthorSuggestView.as_view(), name='author_suggest')

]
urlpatterns += router.urls
