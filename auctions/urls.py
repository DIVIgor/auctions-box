from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (IndexView, GetCategories, GetListingsByCat, GetListing, 
    GetUsersListings, GetBidding, AddListing, AddToWatchlist, GetWatchlist, CloseListing)
from . import views


app_name = 'auctions'

urlpatterns = [
    # listings
    path('', IndexView.as_view(), name='index'),
    # path('', views.index, name="index"),
    path('categories/', GetCategories.as_view(), name='categories'),
    # path('categories/', views.get_categories, name='categories'),
    path('<slug:cat_slug>/',
        GetListingsByCat.as_view(), name='listings'),
    # path('<slug:cat_slug>/',
    #     views.get_listings_by_category, name='listings'),
    path('<slug:cat_slug>/<slug:listing_slug>/',
        GetListing.as_view(), name='listing'),
    # path('<slug:cat_slug>/<slug:listing_slug>/',
    #     views.get_listing, name='listing'),
    # user actions
    path('add_listing', login_required(AddListing.as_view()), name='add_listing'),
    # path('add_listing', views.add_listing, name='add_listing'),
    path('watchlist', login_required(GetWatchlist.as_view()), name='get_watchlist'),
    # path('watchlist', views.get_watchlist, name='get_watchlist'),
    path('<slug:cat_slug>/<slug:listing_slug>/add_to_watchlist',
        login_required(AddToWatchlist.as_view()), name="watch"),
    # path('<slug:cat_slug>/<slug:listing_slug>/add_to_watchlist',
    #     views.add_to_watchlist, name="watch"),
    path('<slug:cat_slug>/<slug:listing_slug>/close_listing',
        login_required(CloseListing.as_view()), name="close_listing"),
    # path('<slug:cat_slug>/<slug:listing_slug>/close_listing',
    #     views.close_listing, name="close_listing"),
    path('my-listings', login_required(GetUsersListings.as_view()), name='get_users_listings'),
    # path('my-listings', views.get_users_listings, name='get_users_listings'),
    path('bidding', login_required(GetBidding.as_view()), name='bidding')
    # path('bidding', views.get_bidding, name='bidding')
]
