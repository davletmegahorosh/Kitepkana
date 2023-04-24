from django.contrib import admin
from django.urls import path
from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/catalog/', views.CatalogApiView.as_view()),
    path('api/v1/catalog/<int:id>/', views.CatalogDetailApiView.as_view()),
    path('api/v1/author/<int:id>/', views.AuthorApiView.as_view()),
    path('api/v1/genre/<int:id>/', views.GenreApiView.as_view())
]


