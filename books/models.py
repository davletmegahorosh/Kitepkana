from django.db import models
from django.urls import reverse

from users.models import User
from .genres_list import GENRE_CHOICES


class Authors(models.Model):
    fullname = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={"pk": self.pk})


class Genres(models.Model):
    genre_name = models.CharField(
        max_length=50,
        help_text='Выбери жанр',
        choices=GENRE_CHOICES)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.genre_name

    def get_absolute_url(self):
        return reverse('genres_detail', kwargs={"pk": self.pk})


class SimilarGenre(models.Model):
    simil_name = models.CharField(max_length=100, null=True)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True, related_name='similar_genres')

    class Meta:
        verbose_name = "Похожий жанр"
        verbose_name_plural = "Похожие жанры"

    def __str__(self):
        return self.simil_name


class Books(models.Model):
    cover = models.ImageField(upload_to='', null=True, blank=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, null=True, blank=True, related_name='author_books')
    summary = models.TextField()
    pages = models.IntegerField()
    genre = models.ManyToManyField(Genres, related_name='genre_books')
    file = models.FileField(upload_to='', null=True, blank=True)

    class Meta:
        ordering = ['cover', 'title', 'author']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def get_absolute_url(self):
        return reverse('books_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return f"{str(self.title)}"

    @property
    def author_name(self):
        return str(self.author)



class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    user = models.CharField("Пользователь", max_length=30)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name="книга", related_name='ratings')

    def __str__(self):
        return f"{self.book} - {self.star} - {self.user}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    text = models.TextField(null=True, blank=True, help_text='Оставь комментарии')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return str(self.book)

    @property
    def get_user(self):
        return str(self.user)

    def get_book(self):
        return str(self.book)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return self.user.username + " borrowed " + self.book.title

    def book_title(self):
        return str(self.book.title)


class ReadingBookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    bookmarked_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Читаю"

    def __str__(self):
        return f'{self.user.username} bookmarked {self.book.title}'


class WillReadBookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    bookmarked_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Буду читать"

    def __str__(self):
        return f'{self.user.username} bookmarked {self.book.title}'




class FinishBookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    bookmarked_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Прочитано"

    def __str__(self):
        return f'{self.user.username} bookmarked {self.book.title}'








