from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Movie, MoviesRating


class MovieAdmin(ModelAdmin):
    model = Movie
    list_display = ["movieId", "title", "director", "writer", "actors", "language", "country","plot","poster","metascore","imdbVotes","imdbRating","imdbID", "genres", "year"]


class MoviesRatingAdmin(ModelAdmin):
    model = MoviesRating
    list_display = ["movie", "user", "rating"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(MoviesRating, MoviesRatingAdmin)
