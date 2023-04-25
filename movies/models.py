from django.db import models
from accounts.models import User
import uuid


class Movie(models.Model):
    title = models.TextField(primary_key=True)
    movieId = models.IntegerField(blank=True)
    genre = models.TextField()
    imdbId = models.IntegerField()
    tmdbId = models.IntegerField()
    timestamp = models.IntegerField(blank=True, null=True)
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
