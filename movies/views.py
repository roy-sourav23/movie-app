from django.views.generic import TemplateView
from accounts.models import User
from movies.models import Movie, MoviesRating
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
from django.shortcuts import redirect
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
        
    """convert genre from mood"""
    def mood_to_genre(self):
        username = self.get_username()
        user = User.objects.get(username=username)
        mood = user.user_mood
        genre = ""
        if mood.lower() == "happy":
            genre= "sci-fi"
        elif mood.lower() == "sad":
            genre = "drama"
        elif mood.lower() == "satisfied":
            genre = "animation"
        elif mood.lower() == "angry":
            genre = "romance"
        elif mood.lower() == "peaceful":
            genre = "fantasy"
        elif mood.lower() == "fearful":
            genre = "adventure"
        elif mood.lower() == "excited":
            genre = "crime"
        elif mood.lower() == "depressed":
            genre = "comedy"
        elif mood.lower() == "content":
            genre = "mystery"
        elif mood.lower() == "sorrowful":
            genre = "action"
        return genre
    
    """returns recommended movie list"""
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

        return recommended_movies

    
    """recommends top 10 movie"""
    def top10recommended(self):
        top10recommended = [] 
        recommended_movies = self.main()
        for movie in recommended_movies :
            if len(movie.title) < 10:
                top10recommended.append(movie)
        if len(top10recommended)> 10:
            return top10recommended[:10]
        return top10recommended
    
    
    """recommends movies based on genre"""
    def get_mood_based_recommendation(self, genre):
        
        top10movies = self.top10recommended()
        mood_movies = []
        recommended_list = self.main()
        for movie in recommended_list:  
            if genre in movie.genres.lower() and len(movie.title)< 30 and movie not in top10movies:
                mood_movies.append(movie)
        if len(mood_movies)<= 10:
            return mood_movies
        return mood_movies[:10]
        
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = self.top10recommended()
        genre = self.mood_to_genre()
        if movies:
            context["movies"] = movies
        context["mood"] = ""
        context["mood_movies"] = self.get_mood_based_recommendation(genre)
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

class MoodPageView(TemplateView):
    template_name = "mood_movies.html"
    success_url = "home"

    def post(self, request, *args, **kwargs):
        if request.POST.get("selected-emoji"):
            selected_emoji = request.POST.get("selected-emoji")
        else:
            selected_emoji = "happy" 
        user = User.objects.get(username=request.user.username)
        user.user_mood = selected_emoji
        user.save()
        return redirect("home")
       