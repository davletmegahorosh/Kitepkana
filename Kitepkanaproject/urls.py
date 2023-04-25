from django.contrib import admin
from django.urls import path
from books import views
from admin import views as adminviews
from Kitepkanaproject.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/catalog/', views.CatalogApiView.as_view()),
    path('api/v1/catalog/<int:id>/', views.CatalogDetailApiView.as_view()),
    path('api/v1/author/', adminviews.AuthorApiView.as_view()),
    path('api/v1/genre/', adminviews.GenreApiView.as_view())
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)