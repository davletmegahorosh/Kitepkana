from django.contrib import admin
from bookmarks.models import *

admin.site.register(ReadingBookMark)
admin.site.register(WillReadBookMark)
admin.site.register(FinishBookMark)

