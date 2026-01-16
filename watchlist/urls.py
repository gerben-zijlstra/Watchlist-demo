from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.movie_search, name="movie_search"),
    path("add/<str:tmdb_id>/", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/", views.my_watchlist, name="my_watchlist"),
]
