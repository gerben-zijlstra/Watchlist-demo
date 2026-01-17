from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.movie_search, name="movie_search"),
    # we need to pass on the correct movie id and watchlist id
    # before we fire the function to add the movie
    path(
        "add/<str:tmdb_id>/<int:list_id>/",
        views.add_to_watchlist,
        name="add_to_watchlist",
    ),
    path("my-lists/", views.my_watchlist, name="my_watchlist"),
]
