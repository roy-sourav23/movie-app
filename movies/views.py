from django.views.generic import TemplateView
import requests
from environs import Env

env = Env()

API_URL = env("OMDB_API_URL")
API_KEY = env("OMDB_API_KEY")


class HomePageView(TemplateView):
    template_name = "home.html"

    def movies(self):
        query = self.request.GET.get("search")
        if not query:
            return {}

        params = {"t": query, "apikey": API_KEY}
        response = requests.get(API_URL, params=params)

        if not response.ok:
            return {}

        data = response.json()
        if data.get("Response") == "False":
            return {}
        return data

    def text_to_list(self, text):
        if "," not in text:
            return text.split(" ")
        names = text.split(",")
        return names

    def mins_to_hrs(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_data = self.movies()

        if movie_data:
            context["movie"] = {
                "title": movie_data.get("Title"),
                "year": movie_data.get("Year"),
                "rated": movie_data.get("Rated"),
                "release_date": movie_data.get("Released"),
                "runtime": movie_data.get("Runtime"),
                "genres": self.text_to_list(movie_data.get("Genre")),
                "director": self.text_to_list(movie_data.get("Director")),
                "writer": self.text_to_list(movie_data.get("Writer")),
                "actors": self.text_to_list(movie_data.get("Actors")),
                "plot": movie_data.get("Plot"),
                "language": self.text_to_list(movie_data.get("Language")),
                "country": self.text_to_list(movie_data.get("Country")),
                "poster": movie_data.get("Poster"),
                "metascore": movie_data.get("Metascore"),
                "imdbRating": movie_data.get("imdbRating"),
                "imdbVotes": movie_data.get("imdbVotes"),
                "imdbID": movie_data.get("imdbID"),
                "boxoffice": movie_data.get("BoxOffice"),
            }

        return context
