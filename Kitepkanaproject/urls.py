from django.contrib import admin
from django.urls import path, include, re_path
from Kitepkanaproject.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # BOOKS
    path('admin/', admin.site.urls),
    path('', include('books.urls')),

    # DEFAULT ADMIN APP
    path('', include('admins.urls')),

    # USER
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('users.urls')),

    # DRF-SPECTACULAR
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='/'))]
# static(MEDIA_URL, document_root=MEDIA_ROOT)

