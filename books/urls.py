from django.urls import path
from .views import BookApiView, AuthorApiView, GenreApiView, AuthorDetailView

urlpatterns = [
    path('api/v1/books/', BookApiView.as_view()),
    path('api/v1/authors/', AuthorApiView.as_view()),
    path('api/v1/genres/', GenreApiView.as_view()),
    path('api/v1/author/<int:id>/', AuthorDetailView.as_view())

]
