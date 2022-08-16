from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (IndexView, GetCategories, GetListingsByCat, GetListing, 
    GetUsersListings, GetBidding, AddListing, AddToWatchlist, GetWatchlist, CloseListing)


app_name = 'auctions'

urlpatterns = [
    # listings
    path('', IndexView.as_view(), name='index'),
    path('categories/', GetCategories.as_view(), name='categories'),
    path('<slug:cat_slug>/',
        GetListingsByCat.as_view(), name='listings'),
    path('<slug:cat_slug>/<slug:listing_slug>/',
        GetListing.as_view(), name='listing'),
    # user actions
    path('add_listing', login_required(AddListing.as_view()), name='add_listing'),
    path('watchlist', login_required(GetWatchlist.as_view()), name='get_watchlist'),
    path('<slug:cat_slug>/<slug:listing_slug>/add_to_watchlist',
        login_required(AddToWatchlist.as_view()), name="watch"),
    path('<slug:cat_slug>/<slug:listing_slug>/close_listing',
        login_required(CloseListing.as_view()), name="close_listing"),
    path('my-listings', login_required(GetUsersListings.as_view()), name='get_users_listings'),
    path('bidding', login_required(GetBidding.as_view()), name='bidding')
]
