import requests
from django.conf import settings
from .models import Movie, Tag


class TMDBService:
    # shortcut, all requests start with this
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

    # running the moment you make an instance of service,
    # grabs key from .env
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY

    # popularity results with pagination, returning top 12
    # using this as fallback when the search is empty
    def get_popular_movies(self):
        url = f"{self.BASE_URL}/trending/movie/day"
        params = {"api_key": self.api_key, "language": "en"}
        response = requests.get(url, params=params)
        return response.json().get("results", [])[:12]

    def search_movies(self, query):
        "fetches results from the API"
        url = f"{self.BASE_URL}/search/movie"
        # checking if the search is empty
        if not query:
            return []

        # passing allow params for TMDB to see that we are a user with key
        params = {
            "api_key": self.api_key,
            "query": query,
            "include-adult": False,
            "language": "en",
        }
        # response to tmdb, getting raw data and preventing crashes with empty list, if nothing is found "[]"
        response = requests.get(url, params=params)
        raw_results = response.json().get("results", [])

        # quality filtering, no adult & sort by popularity
        filtered_results = [
            movie
            for movie in raw_results
            if movie.get("poster_path") and movie.get("overview")
        ]

        # sorting by popularity descending
        # filtered_results.sort(key=lambda x: x.get("popularity", 0), reverse=True)

        return filtered_results

    def get_or_create_movie(self, tmdb_id):
        "fetches full movie details and saves it to movie table if there is not one already existing"
        url = f"{self.BASE_URL}/movie/{tmdb_id}"
        params = {"api_key": self.api_key}
        # converts response into a dict named data
        data = requests.get(url, params=params).json()

        movie, created = Movie.objects.get_or_create(
            # handling the movie record for db saving
            # this is the unique identifier, checks db for this specific id
            external_api_id=str(data["id"]),
            # If it is not existant in the db,
            # django creates a new row with these
            defaults={
                # telling it to combine the movie record and the poster path,
                # if this does not exist, it is None
                "title": data["title"],
                "overview": data.get("overview") or "No description available",
                "poster_url": (
                    f"{self.IMAGE_BASE_URL}{data['poster_path']}"
                    if data["poster_path"]
                    else None
                ),
                "release_date": (data.get("release_date") or None),
                "imdb_rating": data.get("vote_average"),
            },
        )

        # handling the tag, we want to have it pass along it's tags
        # if they don't exist in the db yet, we save them
        if "genres" in data:
            # looping through all the genres
            for genre in data["genres"]:
                # looking for tag with external_tag_id
                # _ I throuw away, since we don't need created_boolean
                tag, _ = Tag.objects.get_or_create(
                    external_tag_id=genre["id"], defaults={"name": genre["name"]}
                )
                # creates a ManyToMany with movie, connects them
                tag.movies.add(movie)
        return movie  # finally returning the result
