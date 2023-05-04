from django.db import models
from users.models import User


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
    cover = models.ImageField(upload_to='')
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, null=True)
    summary = models.TextField()
    pages = models.IntegerField()
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        ordering = ['cover', 'title', 'author']

    def __str__(self):
        return f"{str(self.title)}"
