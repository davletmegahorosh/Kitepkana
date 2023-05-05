from django.contrib import admin
from django.urls import path, include, re_path
from Kitepkanaproject.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]


urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='/'))]
static(MEDIA_URL, document_root=MEDIA_ROOT)