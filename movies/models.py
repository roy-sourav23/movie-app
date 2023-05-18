from django.db import models
from accounts.models import User

class Movie(models.Model):
    title = models.TextField(primary_key=True)
    movieId = models.IntegerField(blank=True)
    rated = models.CharField(max_length=20, blank=True)
    runtime = models.CharField(max_length=20, blank=True)
    genres = models.TextField()
    director = models.TextField()
    writer = models.TextField()
    actors = models.TextField()
    language = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    plot = models.TextField()
    poster = models.URLField()
    metascore = models.CharField(max_length=5)
    imdbVotes = models.CharField(max_length=10)
    imdbRating = models.FloatField()
    imdbID = models.CharField(max_length=10)
    year = models.SmallIntegerField(blank=True, null=True)
    boxoffice = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title

class MoviesRating(models.Model):
    movie = models.ForeignKey(
        Movie, related_name="movie_ratings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="user_ratings", on_delete=models.CASCADE
    )
    rating = models.FloatField(blank=False)

    def __str__(self):
        return f"'{self.movie.title}' ratings"
