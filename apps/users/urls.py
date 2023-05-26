from django.urls import path
from apps.users import views

urlpatterns = [
    path('api/v1/profile/', views.ProfileRetrieveUpdateView.as_view()),
]