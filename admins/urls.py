from django.urls import path, include
from .views import AdminPanelView

urlpatterns = [
     path('api/v1/admin_panel/', AdminPanelView.as_view())
 ]