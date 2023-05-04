from .views import AuthorDetailView, GenreDetailView, BookDetailView
from .views import AuthorListView, GenreListView,BookListView
from .views import AuthorCreateView, GenreCreateView, BookCreateView
from django.urls import path

urlpatterns = [
    path('api/v1/author/create/', AuthorCreateView.as_view()),
    path('api/v1/genre/create/', GenreCreateView.as_view()),
    path('api/v1/book/create/', BookCreateView.as_view()),
    path('api/v1/author/<int:pk>/', AuthorDetailView.as_view()),
    path('api/v1/genre/<int:pk>/', GenreDetailView.as_view()),
    path('api/v1/book/<int:pk>/', BookDetailView.as_view()),
    path('api/v1/authors/', AuthorListView.as_view()),
    path('api/v1/genres/', GenreListView.as_view()),
    path('api/v1/books/', BookListView.as_view())

]



















# from django.urls import path
# from .views import AuthorCreateView, AuthorRetrieveView, AuthorUpdateView, AuthorDestroyView
# from .views import GenreCreateView, GenreRetrieveView, GenreUpdateView, GenreDestroyView
# from .views import BookCreateView, BookRetrieveView, BookUpdateView, BookDestroyView
# from .views import AuthorsListView, GenresListView, BookListView
# from .views import AuthorDetailApiView, GenreDetailApiView
# # Single Objects
# urlpatterns = [
#     path('api/v1/author/create/', AuthorCreateView.as_view()),
#     path('api/v1/author/retrieve/<int:pk>/', AuthorRetrieveView.as_view()),
#     path('api/v1/author/update/<int:pk>/', AuthorUpdateView.as_view()),
#     path('api/v1/author/delete/<int:pk>/', AuthorDestroyView.as_view()),
#     path('api/v1/genre/create/', GenreCreateView.as_view()),
#     path('api/v1/genre/retrieve/<int:pk>/', GenreRetrieveView.as_view()),
#     path('api/v1/genre/update/<int:pk>/', GenreUpdateView.as_view()),
#     path('api/v1/genre/delete/<int:pk>/', GenreDestroyView.as_view()),
#     path('api/v1/book/create/', BookCreateView.as_view()),
#     path('api/v1/book/retrieve/<int:pk>/', BookRetrieveView.as_view()),
#     path('api/v1/book/update/<int:pk>/', BookUpdateView.as_view()),
#     path('api/v1/book/delete/<int:pk>/', BookDestroyView.as_view()),
#     path('api/v1/author/detail/<int:pk>/', AuthorDetailApiView.as_view()),
#     path('api/v1/genre/detail/<int:pk>/', GenreDetailApiView.as_view())
# ]
#
# # Multiple objects
# multiple_views_urlpatterns = [
#     path('api/v1/authors/', AuthorsListView.as_view()),
#     path('api/v1/genres/', GenresListView.as_view()),
#     path('api/v1/books/', BookListView.as_view())
# ]
# urlpatterns += multiple_views_urlpatterns

# urlpatterns = [
#     path('api/v1/books/', BookApiView.as_view()),
#     path('api/v1/authors/', AuthorApiView.as_view()),
#     path('api/v1/genres/', GenreApiView.as_view()),
#     path('api/v1/author/<int:author_id>/', AuthorDetailApiView.as_view()),
#     path('api/v1/genre/<int:genre_id>/', GenreDetailApiView.as_view())
#
# ]
