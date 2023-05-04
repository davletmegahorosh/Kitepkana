from django.urls import path
from .views import AuthorCreateView, AuthorRetrieveView, AuthorUpdateView, AuthorDeleteView
from .views import GenreCreateView, GenreRetrieveView, GenreUpdateView, GenreDeleteView
from .views import BookCreateView, BookRetrieveView, BookUpdateView, BookDeleteView
from .views import BookListView, GenreListView, AuthorListView
urlpatterns = [
    path('api/v1/author/create/<int:pk>/', AuthorCreateView.as_view()),
    path('api/v1/author/retrieve/<int:pk>/', AuthorRetrieveView.as_view()),
    path('api/v1/author/update/<int:pk>/', AuthorUpdateView.as_view()),
    path('api/v1/author/delete/<int:pk>/', AuthorDeleteView.as_view()),
    path('api/v1/genre/create/<int:pk>/', GenreCreateView.as_view()),
    path('api/v1/genre/retrieve/<int:pk>/', GenreRetrieveView.as_view()),
    path('api/v1/genre/update/<int:pk>/', GenreUpdateView.as_view()),
    path('api/v1/genre/delete/<int:pk>/', GenreDeleteView.as_view()),
    path('api/v1/book/create/<int:pk>/', BookCreateView.as_view()),
    path('api/v1/book/retrieve/<int:pk>/', BookRetrieveView.as_view()),
    path('api/v1/book/update/<int:pk>/', BookUpdateView.as_view()),
    path('api/v1/book/delete/<int:pk>/', BookDeleteView.as_view()),
    path('api/v1/books/', BookListView.as_view()),
    path('api/v1/genres/', GenreListView.as_view()),
    path('api/v1/authors/', AuthorListView.as_view())
]

