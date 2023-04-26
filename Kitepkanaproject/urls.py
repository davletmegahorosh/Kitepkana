from django.contrib import admin
from django.urls import path
from Kitepkanaproject.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin.urls')),
    path('',include('books.urls')),
    path('', include('users.urls')),  # Эндпоинты указаны в urls.py приложения users
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
