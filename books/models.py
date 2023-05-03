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
    cover = models.ImageField(upload_to='')
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, related_name='author')
    description = models.CharField(max_length=150)
    pages = models.FloatField()
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, related_name='genre')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def get_author(self):
        return str(self.author)

    @property
    def get_genre(self):
        return str(self.genre)
