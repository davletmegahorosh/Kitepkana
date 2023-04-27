from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Book(models.Model):
    cover = models.ImageField(null=True)
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    description = models.CharField(max_length=150)
    pages = models.IntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')



    def __str__(self):
        return self.name

    @property
    def genre_name(self):
        return self.genre.name

