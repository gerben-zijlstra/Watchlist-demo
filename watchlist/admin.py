from django.contrib import admin
from .models import Movie, Watchlist, WatchlistItem, Tag

admin.site.register(WatchlistItem)
admin.site.register(Watchlist)
admin.site.register(Movie)
admin.site.register(Tag)
# Register your models here.
