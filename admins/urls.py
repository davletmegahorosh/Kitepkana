from django.urls import path, include
from .views import AdminPanelView

urlpatterns = [
     path('admin_panel/', AdminPanelView.as_view(), name='admin_panel')
 ]