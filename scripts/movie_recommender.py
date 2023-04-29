from accounts.models import User
from movies.models import Movie, MoviesRating

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
