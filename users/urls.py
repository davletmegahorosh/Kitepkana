from django.urls import path
from users import views

urlpatterns = [
    path('profile/', views.ProfileRetrieveUpdateView.as_view(), name='profile'),
    path('profile/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
]