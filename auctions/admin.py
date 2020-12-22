from django.contrib import admin

from .models import AuctionListings, Watchlist
# Register your models here.
admin.site.register(AuctionListings)
admin.site.register(Watchlist)
