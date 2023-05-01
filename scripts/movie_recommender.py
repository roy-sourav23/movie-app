from accounts.models import User
from movies.models import Movie, MoviesRating
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
#features = ["title", "genre", "director", "writer", "actors", "language", "country", "plot", "year",]

def get_mood_based_recommendation(genre, recommended_list):
    for movie in recommended_list:
        if genre in movie.genre and len(movie.title) < 20:
            print(movie)

def run():

    """extract list of features for each movie"""
    movies = Movie.objects.all()
    movie_features = [f"{movie.title} {movie.genre} {movie.director} {movie.writer} {movie.actors} {movie.language} {movie.country} {movie.plot} {movie.year}" for movie in movies] 


    """vectorize the movie features """
    vectorizer = TfidfVectorizer()
    movie_vectors = vectorizer.fit_transform(movie_features)
    movie_vector_array = movie_vectors.toarray()

    """compute the similarity matrix"""
    similarity_matrix = cosine_similarity(movie_vectors.toarray())

    
    """select the watched movies"""
    user = User.objects.get(username=7)
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

    # pick the top 6 recommended movies based on rating and number of votes
    recommended_movies = []
    for watched_movie_id, recommended_movies_qs in similar_movies.items():
        for recommended_movie in recommended_movies_qs.order_by("-imdbRating", "-imdbVotes")[:2]:
            if recommended_movie not in recommended_movies:
                recommended_movies.append(recommended_movie)

    get_mood_based_recommendation("Action", recommended_movies)
    for movie in recommended_movies[:6]:
        print(movie.poster)

    
    