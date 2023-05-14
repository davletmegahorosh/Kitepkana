from django.urls import path
from .views import ProfileRetrieveUpdateView

urlpatterns = [
    path('api/v1/profile/', ProfileRetrieveUpdateView.as_view(), name='profile'),
]
