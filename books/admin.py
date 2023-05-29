from django.contrib import admin
<<<<<<< HEAD
from books.models import Books, Authors, Genres
from books.models import Review, Favorite

admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(Genres)
admin.site.register(Review)
admin.site.register(Favorite)
=======
from books.models import Book, Author, Genre


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
>>>>>>> 87932bde6fb07ab19d812637aa03a6c25c48eb2a
