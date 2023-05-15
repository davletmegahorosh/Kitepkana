from django.urls import path, re_path
from .views import AuthorCreateView, AuthorRetrieveView, AuthorUpdateView, AuthorDeleteView
from .views import GenreCreateView, GenreRetrieveView, GenreUpdateView, GenreDeleteView
from .views import BookCreateView, BookRetrieveView, BookUpdateView, BookDeleteView
from .views import BookListView, GenreListView, AuthorListView, ReviewListView, search
from .views import GenreDetailApiView, AuthorDetailApiView, BookDetailApiView, ReviewCreateView, ReviewDeleteView,\
    ReviewUpdateView, FavoriteBooksView, FavoriteListView

urlpatterns = [
    path('api/v1/author/create/', AuthorCreateView.as_view()),
    path('api/v1/author/retrieve/<int:pk>/', AuthorRetrieveView.as_view()),
    path('api/v1/author/update/<int:pk>/', AuthorUpdateView.as_view(), ),
    path('api/v1/author/delete/<int:pk>/', AuthorDeleteView.as_view()),
    path('api/v1/genre/create/', GenreCreateView.as_view()),
    path('api/v1/genre/retrieve/<int:pk>/', GenreRetrieveView.as_view()),
    path('api/v1/genre/update/<int:pk>/', GenreUpdateView.as_view()),
    path('api/v1/genre/delete/<int:pk>/', GenreDeleteView.as_view()),
    path('api/v1/book/create/', BookCreateView.as_view()),
    path('api/v1/book/retrieve/<int:pk>/', BookRetrieveView.as_view()),
    path('api/v1/book/update/<int:pk>/', BookUpdateView.as_view()),
    path('api/v1/book/delete/<int:pk>/', BookDeleteView.as_view()),
    path('api/v1/books/', BookListView.as_view()),
    path('api/v1/genres/', GenreListView.as_view()),
    path('api/v1/authors/', AuthorListView.as_view()),
    path('api/v1/reviews/', ReviewListView.as_view()),
    path('api/v1/author/detail/<int:pk>/', AuthorDetailApiView.as_view()),
    path('api/v1/genre/detail/<int:pk>/', GenreDetailApiView.as_view()),
    path('api/v1/book/detail/<int:pk>/', BookDetailApiView.as_view()),
    path('api/v1/review/create/', ReviewCreateView.as_view()),
    path('api/v1/review/update/<int:pk>/', ReviewUpdateView.as_view()),
    path('api/v1/review/delete/<int:pk>/', ReviewDeleteView.as_view()),
    path('api/v1/search/', search),
    path('api/v1/book/favorite/create/', FavoriteBooksView.as_view()),
    path('api/v1/book/favorites/', FavoriteListView.as_view())

]

