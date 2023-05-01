from django.views.generic import TemplateView
from accounts.models import User
from movies.models import Movie, MoviesRating
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
from environs import Env

env = Env()

API_URL = env("OMDB_API_URL")
API_KEY = env("OMDB_API_KEY")


class SearchPageView(TemplateView):
    template_name = "detailPage.html"

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
                "genres": movie_data.get("Genre"),
                "director": movie_data.get("Director"),
                "writer": movie_data.get("Writer"),
                "actors": movie_data.get("Actors"),
                "plot": movie_data.get("Plot"),
                "language": movie_data.get("Language"),
                "country": movie_data.get("Country"),
                "poster": movie_data.get("Poster"),
                "metascore": movie_data.get("Metascore"),
                "imdbRating": movie_data.get("imdbRating"),
                "imdbVotes": movie_data.get("imdbVotes"),
                "imdbID": movie_data.get("imdbID"),
                "boxoffice": movie_data.get("BoxOffice"),
            }

        return context


class HomePageView(TemplateView):
    model = Movie
    template_name = "home.html"
    
    def get_username(self):
        if self.request.user.is_authenticated:
            return self.request.user.username
        else:
            return "1"

    def get_genre(self):
        
        genre = "action"
        if not genre:
            return {}
        return genre
        
    def get_mood_based_recommendation(self, genre, recommended_list):
        mood_movies = []
        for movie in recommended_list:
            if (genre in movie.genres and len(movie.title) < 20) and len(mood_movies)<10:
                mood_movies.append(mood_movies)
                return mood_movies

    def main(self):

        """extract list of features for each movie"""
        movies = Movie.objects.all()
        movie_features = [f"{movie.title} {movie.genres} {movie.director} {movie.writer} {movie.actors} {movie.language} {movie.country} {movie.plot} {movie.year}" for movie in movies] 


        """vectorize the movie features """
        vectorizer = TfidfVectorizer()
        movie_vectors = vectorizer.fit_transform(movie_features)

        """compute the similarity matrix"""
        similarity_matrix = cosine_similarity(movie_vectors.toarray())

        
        """select the watched movies"""
        username = self.get_username()
        user = User.objects.get(username=username)
        watched_movies_ids = MoviesRating.objects.filter(user=user).values_list("movie_id", flat=True)
        
        """find similar movies for each watched movie"""
        similar_movies = {}
        for watched_movie_id in watched_movies_ids:
            watched_movie = Movie.objects.get(title=watched_movie_id)
            movies_list = list(movies)
            watched_movie_idx = movies_list.index(watched_movie)
            similar_movie_idxs = np.argsort(similarity_matrix[watched_movie_idx])[::-1][:10]
            similar_movies[watched_movie_id] = Movie.objects.filter(
                ~Q(title__in=watched_movies_ids), title__in=[movies_list[idx].title for idx in similar_movie_idxs]
            )

        """recommended movies based on rating and number of votes"""
        recommended_movies = []
        for watched_movie_id, recommended_movies_qs in similar_movies.items():
            for recommended_movie in recommended_movies_qs.order_by("-imdbRating", "-imdbVotes")[:2]:
                if recommended_movie not in recommended_movies:
                    recommended_movies.append(recommended_movie)


        genre = self.get_genre()
        top10recommended = [] 
        self.get_mood_based_recommendation(genre, recommended_movies)
        for movie in recommended_movies :
            if len(movie.title) < 10:
                top10recommended.append(movie)
        if len(top10recommended)> 10:
            return top10recommended[:10]
        return top10recommended

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = self.main()
        if movies:
            context["movies"] = movies
        return context
        

class DetailPageView(TemplateView):
    model = Movie
    template_name = "detailPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs["movieId"]
        movie = Movie.objects.get(movieId=movie_id)
        context["movie"] = movie
        return context

    