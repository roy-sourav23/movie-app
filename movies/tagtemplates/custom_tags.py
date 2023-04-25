from django import template
from movies.models import Movie
import scripts.movie_recommender
register = template.Library()

@register.simple_tag(name="total_movies")
def total_movies():
    return Movie.objects.all().count()

@register.simple_tag
def process_button_value(value):
    return "test"