from django.urls import path
from sync_books.views import synchronize_books

urlpatterns = [
    path('sync-books/', synchronize_books, name='sync_books')

]

