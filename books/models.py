from django.db import models

class Authors(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
    genre_name = models.CharField(max_length=50)


    def __str__(self):
        return self.genre_name


class Books(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    pages = models.FloatField()
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



