from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import (SearchView, IndexView, CategoryView,
    ListingsByCatView, DetailedListingView, AddListingView, WatchlistView,
    AddToWatchlist, CloseListingView, ListingsByOwnerView, BiddingView)


class TestUrls(SimpleTestCase):
    """A test case for auctions urls."""

    def test_search_listing_url(self):
        url = reverse('auctions:search_listing')
        self.assertEqual(resolve(url).func.view_class, SearchView)

    def test_index_url(self):
        url = reverse('auctions:index')
        self.assertEqual(resolve(url).func.view_class, IndexView)

    def test_categories_url(self):
        url = reverse('auctions:categories')
        self.assertEqual(resolve(url).func.view_class, CategoryView)

    def test_listings_url(self):
        url = reverse('auctions:listings', args=['category_slug'])
        self.assertEqual(resolve(url).func.view_class, ListingsByCatView)

    def test_listing_url(self):
        url = reverse('auctions:listing',
            args=['category_slug', 'listing_slug'])
        self.assertEqual(resolve(url).func.view_class, DetailedListingView)

    def test_add_listing_url(self):
        url = reverse('auctions:add_listing')
        self.assertEqual(resolve(url).func.view_class, AddListingView)

    def test_get_watchlist_url(self):
        url = reverse('auctions:get_watchlist')
        self.assertEqual(resolve(url).func.view_class, WatchlistView)

    def test_watch_url(self):
        url = reverse('auctions:watch',
            args=['category_slug', 'listing_slug'])
        self.assertEqual(resolve(url).func.view_class, AddToWatchlist)

    def test_close_listing_url(self):
        url = reverse('auctions:close_listing',
            args=['category_slug', 'listing_slug'])
        self.assertEqual(resolve(url).func.view_class, CloseListingView)

    def test_get_users_listings_url(self):
        url = reverse('auctions:get_users_listings')
        self.assertEqual(resolve(url).func.view_class, ListingsByOwnerView)

    def test_bidding_url(self):
        url = reverse('auctions:bidding')
        self.assertEqual(resolve(url).func.view_class, BiddingView)
