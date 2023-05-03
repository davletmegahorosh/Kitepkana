from django.urls import path
from .views import BookApiView, AuthorApiView, GenreApiView

urlpatterns = [
    path('api/v1/book/', BookApiView.as_view()),
    path('api/v1/author/', AuthorApiView.as_view()),
    path('api/v1/genre/', GenreApiView.as_view()),
]
