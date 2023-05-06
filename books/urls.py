from django.urls import path
from books import views
from admins import views as adminviews

urlpatterns = [
    path('api/v1/catalog/', views.CatalogApiView.as_view()),
    path('api/v1/catalog/<int:id>/', views.CatalogDetailApiView.as_view()),
    path('api/v1/author/', adminviews.AuthorApiView.as_view()),
    path('api/v1/genre/', adminviews.GenreApiView.as_view()),
]
