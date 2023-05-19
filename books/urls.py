from django.urls import path, include
from rest_framework import routers
from .views import AuthorViewSet, GenreViewSet, BookViewSet, ReviewViewSet, search,\
    FavoriteViewSet

router = routers.SimpleRouter()
router.register(r'api/v1/authors', AuthorViewSet)
router.register(r'api/v1/genres', GenreViewSet)
router.register(r'api/v1/books', BookViewSet)
router.register(r'api/v1/reviews', ReviewViewSet)
router.register(r'api/v1/favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/search/', search),

]

