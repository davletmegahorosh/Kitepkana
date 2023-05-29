from django.urls import path, include
from rest_framework import routers
from .views import AuthorViewSet, GenreViewSet, BookViewSet, ReviewViewSet, search,\
    FavoriteViewSet, GenreFilterAPIView, TitleFilterAPIView, AuthorFilterAPIView, ReadingBookMarkAPIView, \
    WillReadBookMarkAPIView, FinishBookMarkAPIView, SimilarGenreView, GenreSuggestView, TitleSuggestView, \
    AuthorSuggestView

router = routers.SimpleRouter()
router.register(r'api/v1/authors', AuthorViewSet)
router.register(r'api/v1/genres', GenreViewSet)
router.register(r'api/v1/books', BookViewSet)
router.register(r'api/v1/reviews', ReviewViewSet)
router.register(r'api/v1/favorites', FavoriteViewSet, basename='favorites')


urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/search/', search),
    path('api/v1/genres_filter/', GenreFilterAPIView.as_view(), name='genres_filter'),
    path('api/v1/authors_filter/', AuthorFilterAPIView.as_view(), name='authors_filter'),
    path('api/v1/titles_filter/', TitleFilterAPIView.as_view(), name='titles_filter'),
    path('api/v1/read_bookmark/', ReadingBookMarkAPIView.as_view(), name='read_bookmark'),
    path('api/v1/will_read_bookmark/', WillReadBookMarkAPIView.as_view(), name='will_read_bookmark'),
    path('api/v1/finish_bookmark/', FinishBookMarkAPIView.as_view(), name='finish_bookmark'),
    path('api/v1/alike_genre/', SimilarGenreView.as_view(),  name='alike_genre'),
    path('api/v1/genre_suggest/', GenreSuggestView.as_view(), name='genre_suggest'),
    path('api/v1/title_suggest/', TitleSuggestView.as_view(), name='title_suggest'),
    path('api/v1/author_suggest/', AuthorSuggestView.as_view(), name='author_suggest')

]

