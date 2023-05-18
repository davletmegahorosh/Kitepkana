from django.urls import path
from book_progress.views import book_progress

urlpatterns = [
    path('books/<int:book_id>/progress/', book_progress, name='book-progress')
]
