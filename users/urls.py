from django.urls import path
from .views import AuthorizationApiView, RegistrationApiView

urlpatterns = [
    path('api/v1/users/auth/', AuthorizationApiView.as_view()),
    path('api/v1/users/reg/', RegistrationApiView.as_view())
]
