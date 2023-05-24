from django.urls import path
from users import views

urlpatterns = [
    path('api/v1/profile/', views.ProfileRetrieveUpdateView.as_view()),
    path('api/v1/profile/delete/', views.ProfileDeleteView.as_view()),
]