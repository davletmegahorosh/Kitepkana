from django.contrib import admin
from django.urls import path
from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/catalog/', views.CatalogApiView.as_view()),
    path('api/v1/catalog/<int:pk>/', views.CatalogDetailApiView.as_view()),
    path('api/v1/catalog/genre/', views.CatalogGenreApiView.as_view()),
    path('api/v1/catalog/author/', views.CatalogAuthorApiView.as_view()),
]
