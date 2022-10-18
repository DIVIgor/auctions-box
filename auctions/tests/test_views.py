from unittest import skip
from django.test import TestCase
from django.urls import reverse, resolve

from account.models import User
from ..models import Category, Listing, Bid, Comment, Watchlist
from ..views import (CategoryView, SearchView, IndexView, ListingsByCatView,
    DetailedListingView, ListingsByOwnerView, BiddingView, AddListingView,
    AddToWatchlist, WatchlistView, CloseListingView)


class BaseTestViewMethodsMixin:
    """A base mixin of test methods for views.
    Contains functions:
        - `test_context_object_name`
        - `test_view_url_exists_at_desired_location`
        - `test_view_uses_correct_template`
    """

    def test_context_object_name(self):
        self.assertIn(self.context_name, self.resp.context)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(self.location)
        print(resp.request)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.resp, self.template_name)

class ListingTestViewMethodsMixin:
    """A mixin of test methods for views that return listings.
    Contains functions:
    """

    def test_view_lists_only_active_listings(self):
        for listing in self.resp.context[self.context_name]:
            self.assertTrue(listing.is_active)

    def test_pagination_is_correct(self):
        self.assertTrue(self.resp.context['is_paginated'])
        self.assertEqual(len(self.resp.context[self.context_name]), self.paginated_by)

class TestCategoryView(BaseTestViewMethodsMixin, TestCase):
    """A test case for Category View."""

    @classmethod
    def setUpTestData(cls):
        category_num = 10
        for category in range(category_num):
            Category.objects.create(name=f'Cat {category}',
                slug=f'cat-{category}')

    def setUp(self):
        self.location = '/categories/'
        self.context_name = 'categories'
        self.template_name = 'auctions/categories.html'
        self.resp = self.client.get(reverse('auctions:categories'))

    def test_view_lists_all_categories(self):
        self.assertEqual(len(self.resp.context[self.context_name]), 10)

class TestSearchView(
        ListingTestViewMethodsMixin, BaseTestViewMethodsMixin, TestCase):
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
                start_bid = listing
            )

    def setUp(self):
        self.paginated_by = 15
        self.location = '/search/'
        self.context_name = 'listing_search'
        self.template_name = 'auctions/listing_search.html'
        self.resp = self.client.get(reverse('auctions:search_listing'))

    def test_result_lists_searched_listings(self):
        search = 7
        resp = self.client.get('/search/', {'q': f'{search}'})
        self.assertEqual(len(resp.context[self.context_name]), 1)
        self.assertIn(f'{search}', resp.context[self.context_name][0].name)
        self.assertIn(f'{search}',
            resp.context[self.context_name][0].description)

    @skip
    def test_view_lists_only_active_listings(self):
        pass

class TestIndexView(
        ListingTestViewMethodsMixin, BaseTestViewMethodsMixin, TestCase):
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
                start_bid = listing,
                is_active = listing % 2
            )

    def setUp(self):
        self.paginated_by = 15
        self.location = ''
        self.context_name = 'active_listings'
        self.template_name = 'auctions/index.html'
        self.resp = self.client.get(reverse('auctions:index'))

class TestListingsByCatView(
        ListingTestViewMethodsMixin, BaseTestViewMethodsMixin, TestCase):
    """A test case for Listings by Category View."""

    @classmethod
    def setUpTestData(cls):
        listing_num = 35
        for num in range(2):
            Category.objects.create(name=f'Cat {num}', slug=f'cat-{num}')
        User.objects.create(username='Tester')

        for listing in range(listing_num):
            Listing.objects.create(
                category = Category.objects.get(name=f'Cat {listing % 2}'),
                user = User.objects.get(username='Tester'),
                name = f'Listing {listing}',
                slug = f'listing-{listing}',
                description = f'A description for test {listing}.',
                start_bid = listing,
                is_active = listing % 2
            )

    def setUp(self):
        self.paginated_by = 15
        self.cat_slug = 'cat-1'
        self.location = '/cat-1/'
        self.context_name = 'listings'
        self.template_name = 'auctions/listings_by_cat.html'
        self.resp = self.client.get(reverse('auctions:listings', args=[self.cat_slug]))

    def test_view_lists_only_listings_by_desired_category(self):
        for listing in self.resp.context[self.context_name]:
            self.assertEqual(listing.category.slug, self.cat_slug)

class TestListingsByOwnerView(
        ListingTestViewMethodsMixin, BaseTestViewMethodsMixin, TestCase):
    """A test case for Listings by Owner View."""

    @classmethod
    def setUpTestData(cls):
        listing_num = 25
        Category.objects.create(name='Cat', slug='cat')
        User.objects.create_user(username='Tester')

        for listing in range(listing_num):
            Listing.objects.create(
                category = Category.objects.get(name='Cat'),
                user = User.objects.get(username='Tester'),
                name = f'Listing {listing}',
                slug = f'listing-{listing}',
                description = f'A description for test {listing}.',
                start_bid = listing
            )

    def setUp(self):
        self.user = User.objects.get(username='Tester')
        self.paginated_by = 20
        self.location = '/my-listings/'
        self.context_name = 'users_listings'
        self.template_name = 'auctions/users_listings.html'

        self.client.force_login(self.user)
        self.resp = self.client.get(reverse('auctions:get_users_listings'))

    @skip
    def test_view_url_exists_at_desired_location(self):
        pass

    def test_view_lists_only_listings_by_desired_user(self):
        for listing in self.resp.context[self.context_name]:
            self.assertEqual(listing.user, self.user)
