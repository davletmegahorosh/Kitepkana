from django.urls import path
from admin import views

urlpatterns = [
    path('api/v1/author/', views.AuthorApiView.as_view()),
    path('api/v1/genre/', views.GenreApiView.as_view()),
]