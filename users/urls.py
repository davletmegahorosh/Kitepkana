from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from users import views
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from django.urls import re_path
from users.views import CustomDjoserViewSet

router = DefaultRouter()
router.register("users", views.CustomDjoserViewSet)

User = get_user_model()

urlpatterns = [
    path('profile/', views.ProfileRetrieveUpdateView.as_view(), name='profile'),
    path('profile/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
    re_path(r"^jwt/create/?", TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^jwt/refresh/?", TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^jwt/verify/?", TokenVerifyView.as_view(), name="jwt-verify"),
]
urlpatterns += router.urls
