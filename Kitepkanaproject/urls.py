from django.contrib import admin
from django.urls import path, include, re_path
from Kitepkanaproject.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .yasg import urlpatterns as url_yasg

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('books.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('users.urls')),
=======
    path('api/v1/catalog/', views.CatalogApiView.as_view()),
    path('api/v1/catalog/<int:pk>/', views.CatalogDetailApiView.as_view()),
    path('api/v1/author/', views.AuthorApiView.as_view()),
    path('api/v1/genre/', views.GenreApiView.as_view())
>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a
]

urlpatterns+=url_yasg

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='/'))]
static(MEDIA_URL, document_root=MEDIA_ROOT)