from django.contrib import admin
from books.models import Books, Authors, Genres
from books.models import Review, Favorite, SimilarGenre
from books.models import ReadingBookMark, WillReadBookMark, FinishBookMark

admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(Genres)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(SimilarGenre)
admin.site.register(ReadingBookMark)
admin.site.register(WillReadBookMark)
admin.site.register(FinishBookMark)

