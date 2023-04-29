from movies.models import Movie, MoviesRating
from accounts.models import User
import csv
import random
import string
import os
import secrets
import time         # delete


static_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
file_path = os.path.join(static_root, 'files', 'data.csv')

"""Function to generate a random email ID"""
def generate_email_id():
    username = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    domain = "".join(random.choices(string.ascii_lowercase, k=5))
    tld = random.choice(["com", "org", "net", "in", "tech", "biz", "ch"])
    email_id = f"{username}@{domain}.{tld}"
    return email_id

def generate_password():
    return secrets.token_urlsafe(16)

# headers 
# movieId, title, genres, userId, rating, timestamp, Director, Writer, Actors,
#  Plot, Language, Country, Poster, Metascore, imdbVotes, imdbRating, imdbID


def run():
    t1 = time.time()     # delete
    """populating database using csvfile"""
    try:
        with open(f"{file_path}", "r") as file:
            rows = csv.DictReader(file)
            Rating = []
            for row in rows:
                """Get an existing movie object or create one """
                movie = Movie.objects.filter(movieId=row["movieId"]).first()
                if movie is None:
                    movie = Movie(
                        movieId = row["movieId"],
                        title = row["title"][:-7],
                        genre = row["genres"],
                        director = row["Director"],
                        writer = row["Writer"],
                        actors = row["Actors"], 
                        language = row["Language"],
                        country = row["Country"],
                        plot = row["Plot"],
                        poster = row["Poster"],
                        metascore = row["Metascore"],
                        imdbVotes = row["imdbVotes"],
                        imdbRating  = row["imdbRating"],
                        imdbID = row["imdbID"],
                        year = int(row["title"][-5:-1]),
                        timestamp = row["timestamp"],
                    )
                    movie.save()
                    
                email = generate_email_id()
                username = row["userId"]
                
                """Get an existing user or create one"""
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User.objects.create(username=row["userId"], email=email, password=generate_password())
               
                """Create a MoviesRating object""" 
                try:
                    rating = MoviesRating.objects.get(movie = movie, user = user, rating = row["rating"])
                except MoviesRating.DoesNotExist:
                    rating = MoviesRating(
                        movie = movie,
                        user = user,
                        rating = row["rating"]
                    )
                    Rating.append(rating)
            MoviesRating.objects.bulk_create(Rating)
        print("Data from CSV file has been imported into the database.")

    except Exception as e:
        print("Error:", e)
    
    t2 = time.time()        # delete 
    time_difference = t2 - t1

    # Convert time difference to minutes, hours, and seconds
    time_difference_minutes = int(time_difference / 60)
    time_difference_hours = int(time_difference / 3600)
    time_difference_seconds = int(time_difference % 60)

    
    print("Time Difference:", time_difference_hours, "hours", time_difference_minutes, "minutes", time_difference_seconds, "seconds")