from django.urls import path
from books import views
from admin import views as adminviews

urlpatterns = [
    path('api/v1/catalog/', views.CatalogApiView.as_view()),
    path('api/v1/catalog/<int:pk>/', views.CatalogDetailApiView.as_view()),
    path('api/v1/author/', adminviews.AuthorApiView.as_view()),
    path('api/v1/genre/', adminviews.GenreApiView.as_view()),
    path('api/v1/genre/<int:pk>/', adminviews.GenreDetailApiView.as_view()),
    path('api/v1/author/<int:pk>/', adminviews.AuthorDetailApiView.as_view())
]
