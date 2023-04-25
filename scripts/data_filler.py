from movies.models import Movie, MoviesRating
from accounts.models import User
import csv
import random
import string
import os

import time         # delete

static_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
file_path = os.path.join(static_root, 'files', 'movies_data_final.csv')

# Function to generate a random email ID
def generate_email_id():
    username = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    domain = "".join(random.choices(string.ascii_lowercase, k=5))
    tld = random.choice(["com", "org", "net", "in", "tech", "biz", "ch"])
    email_id = f"{username}@{domain}.{tld}"
    return email_id

def run():
    t1 = time.time()     # delete
    try:
        with open(f"{file_path}", "r") as file:
            reader = csv.DictReader(file)
            Rating = []
            for row in reader:
                movie = Movie.objects.filter(movieId=row["movieId"]).first()
                if movie is None:
                    movie = Movie(
                        movieId = row["movieId"],
                        title = row["title"],
                        genre = row["genres"],
                        imdbId = row["imdbId"],
                        tmdbId = row["tmdbId"],
                        timestamp = row["timestamp"]
                    )
                    movie.save()

                email = generate_email_id()
                username = row["userId"]
                
                # Get an existing one or create one
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User.objects.create(username=row["userId"], email=email)
               
                # Create a MoviesRating object 
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