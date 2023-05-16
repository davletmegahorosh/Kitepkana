from django.db import models
from django.contrib.auth.models import User
from kitepkana.books.models import Books


class ReadingBookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    bookmarked_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.username} bookmarked {self.book.title}'


class WillReadBookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} bookmarked {self.book.title}'


class FinishBookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} bookmarked {self.book.title}'

