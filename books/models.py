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
    cover = models.ImageField()
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    pages = models.FloatField()
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=(
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ), default=5)

    @property
    def get_rate(self):
        return self.rate


    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, blank=True, related_name='book')
    text = models.TextField()


    def get_book(self):
        return str(self.book)


    def __str__(self):
        return f'book: {self.book}, review: {self.text}'

