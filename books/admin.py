from django.contrib import admin
from books.models import Books, Authors, Genres, Review


admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(Genres)
admin.site.register(Review)

