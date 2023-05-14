from django.db import models
from users.models import User
# from django.contrib.auth.models import User


class Authors(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name', 'surname']

    def __str__(self):
        return self.name


class Genres(models.Model):
    genre_name = models.CharField(
        max_length=50,
        help_text='Вводи название жанра(Например, Хоррор, Романтика и.т.д')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.genre_name


class Books(models.Model):
    cover = models.ImageField(upload_to='', null=True, blank=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, null=True, related_name='author')
    summary = models.TextField()
    pages = models.IntegerField()
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True, related_name='genre')
    file = models.FileField(upload_to='', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    rate = models.IntegerField(choices=(
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ), default=5)

    class Meta:
        ordering = ['cover', 'title', 'author']

    def __str__(self):
        return f"{str(self.title)}"

    @property
    def author_name(self):
        return str(self.author)

    @property
    def genre_name(self):
        return str(self.genre)


class Review(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, blank=True, related_name='book')
    review_text = models.TextField(null=True, blank=True, help_text='Оставь комментарии')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

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
    def __str__(self):
        return self.user.username + " borrowed " + self.book.title