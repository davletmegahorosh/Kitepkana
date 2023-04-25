from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)


    def __str__(self):
        return self.genre_name


class Book(models.Model):
    cover = models.ImageField(null=True)
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    pages = models.FloatField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



