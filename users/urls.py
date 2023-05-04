from django.urls import path
<<<<<<< HEAD
from .views import RegisterView, LoginView, LogoutView, AllUserView
urlpatterns = [
    path('api/v1/register/', RegisterView.as_view()),
    path('api/v1/login/', LoginView.as_view()),
    path('api/v1/logout/', LogoutView.as_view()),
    path('api/v1/users/', AllUserView.as_view()),
]
=======


>>>>>>> Dev
