from django.test import TestCase
from django.urls import reverse, resolve

from auctions.views import (CategoryView, SearchView, IndexView, ListingsByCatView,
    DetailedListingView, ListingsByOwnerView, BiddingView, AddListingView,
    AddToWatchlist, WatchlistView, CloseListingView)


class TestViews(TestCase):
    """A test case for auctions views."""

    def test_category_view(self):
        pass