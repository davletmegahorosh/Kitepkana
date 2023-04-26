from django.urls import path
from books import views

urlpatterns = [
    path('api/v1/catalog/', views.CatalogApiView.as_view()),
    path('api/v1/catalog/<int:id>/', views.CatalogDetailApiView.as_view()),
    ]