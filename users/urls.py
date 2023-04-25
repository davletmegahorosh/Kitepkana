from django.urls import path
from .views import AuthorizationApiView

urlpatterns = [
    path('api/v1/users/auth/', AuthorizationApiView.as_view())
]