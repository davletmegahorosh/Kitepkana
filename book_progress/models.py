from django.db import models
from django.contrib.auth.models import User
from kitepkana.books.models import Books


class BookProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    current_page = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}'s progress for {self.book.title}"

