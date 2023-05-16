from django.urls import path
from .views import ReadingBookMarkAPIView, WillReadBookMarkAPIView, FinishBookMarkAPIView


urlpatterns = [
    path('r_bookmarks/', ReadingBookMarkAPIView.as_view(), name='r_bookmarks'),
    path('will_read_bookmarks/', WillReadBookMarkAPIView.as_view(), name='will_read_bookmarks'),
    path('finish_bookmarks/', FinishBookMarkAPIView.as_view(), name='finish_bookmarks')

]
