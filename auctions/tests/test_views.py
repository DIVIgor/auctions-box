from django.test import TestCase
from django.urls import reverse, resolve

from account.models import User
from ..models import Category, Listing, Bid, Comment, Watchlist
from ..views import (CategoryView, SearchView, IndexView, ListingsByCatView,
    DetailedListingView, ListingsByOwnerView, BiddingView, AddListingView,
    AddToWatchlist, WatchlistView, CloseListingView)


class TestCategoryView(TestCase):
    """A test case for Category View."""

    @classmethod
    def setUpTestData(cls):
        category_num = 10
        for category in range(category_num):
            Category.objects.create(name=f'Cat {category}', 
                slug=f'cat-{category}')

    def setUp(self):
        self.context = 'categories'
        self.resp = self.client.get(reverse('auctions:categories'))

    def test_context_object_name(self):
        self.assertIn(self.context, self.resp.context)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/categories/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.resp, 'auctions/categories.html')

    def test_view_lists_all_categories(self):
        self.assertEqual(len(self.resp.context[self.context]), 10)

class TestSearchView(TestCase):
    """A test case for Search View."""

    @classmethod
    def setUpTestData(cls):
        listing_num = 20
        Category.objects.create(name='Cat 1', slug='cat-1')
        User.objects.create(username='Tester')

        for listing in range(listing_num):
            Listing.objects.create(
                category = Category.objects.get(name='Cat 1'),
                user = User.objects.get(username='Tester'),
                name = f'Listing {listing}',
                slug = f'listing-{listing}',
                description = f'A description for test {listing}.',
                start_bid = 10.95 + listing
            )

    def setUp(self):
        self.context = 'listing_search'
        self.resp = self.client.get(reverse('auctions:search_listing'))

    def test_context_object_name(self):
        self.assertIn(self.context, self.resp.context)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/search/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.resp, 'auctions/listing_search.html')

    def test_result_lists_searched_listings(self):
        search = 7
        resp = self.client.get(f'/search/?q={search}')
        self.assertEqual(len(resp.context[self.context]), 1)
        self.assertIn(f'{search}', resp.context[self.context][0].name)
        self.assertIn(f'{search}', resp.context[self.context][0].description)

    def test_pagination_is_fifteen(self):
        self.assertTrue(self.resp.context['is_paginated'])
        self.assertEqual(len(self.resp.context[self.context]), 15)

class TestIndexView(TestCase):
    """A test case for Index View."""

    @classmethod
    def setUpTestData(cls):
        listing_num = 35
        Category.objects.create(name='Cat 1', slug='cat-1')
        User.objects.create(username='Tester')

        for listing in range(listing_num):
            Listing.objects.create(
                category = Category.objects.get(name='Cat 1'),
                user = User.objects.get(username='Tester'),
                name = f'Listing {listing}',
                slug = f'listing-{listing}',
                description = f'A description for test {listing}.',
                start_bid = 10.95 + listing,
                is_active = listing % 2
            )

    def setUp(self):
        self.resp = self.client.get(reverse('auctions:index'))
        self.context = 'active_listings'

    def test_context_object_name(self):
        self.assertIn(self.context, self.resp.context)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        # self.assertIsInstance(resp.context['view'], IndexView)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.resp, 'auctions/index.html')

    def test_view_lists_only_active_listings(self):
        for listing in self.resp.context[self.context]:
            self.assertTrue(listing.is_active)

    def test_pagination_is_fifteen(self):
        self.assertTrue(self.resp.context['is_paginated'])
        self.assertEqual(len(self.resp.context[self.context]), 15)
