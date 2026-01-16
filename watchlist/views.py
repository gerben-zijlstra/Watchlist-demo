from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .services import TMDBService
from .models import Watchlist, WatchlistItem
from django.contrib import messages


def movie_search(request):
    # gets the q, search from the form
    query = request.GET.get("q")
    results = []
    service = TMDBService()

    if query:
        # calls a method in service
        results = service.search_movies(query)
        message = f"Results for '{query}'"
    else:
        results = service.get_popular_movies()
        message = "Popular Movies"

    return render(
        request, "search_results.html", {"results": results, "message": message}
    )


@login_required
def add_to_watchlist(request, tmdb_id):
    if request.method == "POST":
        # if user wants to add movie by using the button,
        # the service will use the save or get movie function
        service = TMDBService()
        movie = service.get_or_create_movie(tmdb_id)

        # getting the users watchlist or making a default one
        # have to implement*
        watchlist, created = Watchlist.objects.get_or_create(
            # making sure user owns the watchlist
            user=request.user,
            # default name
            name="My Watchlist",
        )

        WatchlistItem.objects.get_or_create(watchlist=watchlist, movie=movie)
        return redirect("my_watchlist")
    return redirect("my_watchlist")


@login_required
def my_watchlist(request):
    # gettings users's watchlist, or create if empty
    watchlist, created = Watchlist.objects.get_or_create(
        user=request.user, name="My Watchlist"
    )
    items = watchlist.items.all().select_related("movie")

    return render(request, "my_watchlist.html", {"items": items})
