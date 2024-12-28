from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    length = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()

    def __str__(self):
        #movie: Movie = self.movie
        return f"{self.name} - {self.movie.title}"
