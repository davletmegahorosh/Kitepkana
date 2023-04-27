from django.urls import path
from users import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('authorization', views.authorization, name='authorization'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
]
