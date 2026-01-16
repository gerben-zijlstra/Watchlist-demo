from django.db import models
from django.contrib.auth.models import User

# used for
from django.core.validators import MinValueValidator, MaxValueValidator


# --- GLOBAL MOVIE DATA ---
class Movie(models.Model):
    """Stores global Metadata cached from TMDB API"""

    external_api_id = models.CharField(max_length=50, unique=True)  # TMDB ID
    title = models.CharField(max_length=255)
    poster_url = models.URLField(max_length=500, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    imdb_rating = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    # background sync
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# --- GENRES / TAGS ---
class Tag(models.Model):
    """Movie Genres fetched automatically from API"""

    external_tag_id = models.IntegerField(
        unique=True, null=True, blank=True
    )  # TMDB Genre ID
    name = models.CharField(max_length=50, unique=True)
    movies = models.ManyToManyField(Movie, related_name="tags")

    def __str__(self):
        return self.name


# --- USER CONTAINERS ---
class Watchlist(models.Model):
    """The 'Folders' (e.g. 'Anime', 'Favorites') owned by a User"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# --- JUNCTION TABLE ---
class WatchlistItem(models.Model):
    """The specific link between a Movie and a User's Watchlist"""

    STATUS_CHOICES = [
        ("planned", "Plan to Watch"),
        ("watching", "Currently Watching"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]
    watchlist = models.ForeignKey(
        Watchlist, on_delete=models.CASCADE, related_name="items"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents adding the same movie to the same list twice
        unique_together = ("watchlist", "movie")


# --- REVIEWS ---
class Rating(models.Model):
    """A User's personal 1-10 score and comment on a Movie"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures one unique review per user, per movie
        unique_together = ("user", "movie")
