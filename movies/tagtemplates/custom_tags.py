from django import template
from movies.models import Movie, MoviesRating
from accounts.models import User, userProfile
register = template.Library()

def get_current_user(request):
    return request.user

@register.simple_tag(name="total_movies")
def total_movies():
    return Movie.objects.all().count()

@register.filter(name="text_to_list")
def text_to_list(text): 
    if isinstance(text, list):
        return text
    elif isinstance(text, str):
        if "," in text:
            return text.split(",")
        elif "|" in text:
            return text.split("|")
    return [text]

@register.filter(name="no_metascore")
def no_metascore(score):
    if not score:
        return "N/A"
    return score[0:2]

@register.filter(name="movie_title")
def movie_title(title):
    if "," in title:
        movie = title.split(",")
        return movie[1]+ " "+ movie[0]
    return title

