from search_hints.views import BookSearchHintsView, AuthorSearchAPIView, GenreSearchAPIView, TitleSearchAPIView
from django.urls import path


urlpatterns = [
    path('search_hints/', BookSearchHintsView.as_view(), name='search-hints'),
    path('author_filter/', AuthorSearchAPIView.as_view(), name='author-filter'),
    path('genre_filter/', GenreSearchAPIView.as_view(), name='genre-filter'),
    path('title_filter/', TitleSearchAPIView.as_view(), name='title-filter')

]

