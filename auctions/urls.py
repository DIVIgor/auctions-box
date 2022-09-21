from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (IndexView, CategoryView, ListingsByCatView,
    DetailedListingView, ListingsByOwnerView, BiddingView, AddListingView,
    AddToWatchlist, WatchlistView, CloseListingView, SearchView)


app_name = 'auctions'

urlpatterns = [
    # listings
    path('search/', SearchView.as_view(), name='search_listing'),
    path('', IndexView.as_view(), name='index'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('<slug:cat_slug>/',
        ListingsByCatView.as_view(), name='listings'),

    path('<slug:cat_slug>/<slug:listing_slug>/',
        DetailedListingView.as_view(), name='listing'),

    # user actions
    path('add_listing', login_required(AddListingView.as_view()),
        name='add_listing'),

    path('watchlist', login_required(WatchlistView.as_view()),
        name='get_watchlist'),

    path('<slug:cat_slug>/<slug:listing_slug>/add_to_watchlist',
        login_required(AddToWatchlist.as_view()), name="watch"),

    path('<slug:cat_slug>/<slug:listing_slug>/close_listing',
        login_required(CloseListingView.as_view()), name="close_listing"),

    path('my-listings', login_required(ListingsByOwnerView.as_view()),
        name='get_users_listings'),

    path('bidding', login_required(BiddingView.as_view()), name='bidding'),
]
