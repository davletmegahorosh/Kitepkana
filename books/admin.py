from django.contrib import admin
from books.models import Book, Author, Genre


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
