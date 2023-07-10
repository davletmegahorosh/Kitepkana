from django.contrib import admin
from books.models import Books, Authors, Genres
from books.models import Review, Favorite, Rating, RatingStar, Page
from books.models import ReadingBookMark, WillReadBookMark, FinishBookMark, Progress
admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(Genres)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(ReadingBookMark)
admin.site.register(WillReadBookMark)
admin.site.register(FinishBookMark)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Page)
admin.site.register(Progress)


