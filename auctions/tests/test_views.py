from unittest import skip, skipIf
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..models import Category, Listing, Bid, Comment, Watchlist

User = get_user_model()


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
        self.assertEqual(resp.status_code, self.status_code)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.resp, self.template_name)

class ListingTestViewMethodsMixin:
    """A mixin of test methods for views that return listings.
    Contains functions:
        - `test_view_lists_only_active_listings`
        - `test_pagination_is_correct`
    """

    def test_view_lists_only_active_listings(self):
        for listing in self.resp.context[self.context_name]:
            self.assertTrue(listing.is_active)

    def test_pagination_is_correct(self):
        self.assertTrue(self.resp.context['is_paginated'])
        self.assertEqual(len(
            self.resp.context[self.context_name]), self.paginated_by)

class TestCategoryView(BaseTestViewMethodsMixin, TestCase):
    """A test case for Category View."""

    @classmethod
    def setUpTestData(cls):
        category_num = 10
        for category in range(category_num):
            Category.objects.create(
                name=f'Cat {category}', slug=f'cat-{category}')

    def setUp(self):
        self.status_code = 200
        self.location = '/categories/'
        self.context_name = 'categories'
        self.template_name = 'auctions/categories.html'
        self.resp = self.client.get(reverse('auctions:categories'))

    def test_view_lists_all_categories(self):
        self.assertEqual(len(self.resp.context[self.context_name]), 10)

class TestSearchView(
        BaseTestViewMethodsMixin, ListingTestViewMethodsMixin, TestCase):
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
                start_bid = listing)

    def setUp(self):
        self.status_code = 200
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
        BaseTestViewMethodsMixin, ListingTestViewMethodsMixin, TestCase):
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
                is_active = listing % 2)

    def setUp(self):
        self.status_code = 200
        self.paginated_by = 15
        self.location = ''
        self.context_name = 'active_listings'
        self.template_name = 'auctions/index.html'
        self.resp = self.client.get(reverse('auctions:index'))

class TestListingsByCatView(
        BaseTestViewMethodsMixin, ListingTestViewMethodsMixin, TestCase):
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
                is_active = listing % 2)

    def setUp(self):
        self.status_code = 200
        self.paginated_by = 15
        self.cat_slug = 'cat-1'
        self.location = f'/{self.cat_slug}/'
        self.context_name = 'listings'
        self.template_name = 'auctions/listings_by_cat.html'
        self.resp = self.client.get(reverse('auctions:listings', args=[self.cat_slug]))

    def test_view_lists_only_listings_by_desired_category(self):
        for listing in self.resp.context[self.context_name]:
            self.assertEqual(listing.category.slug, self.cat_slug)

class TestListingsByOwnerView(
        BaseTestViewMethodsMixin, ListingTestViewMethodsMixin, TestCase):
    """A test case for Listings by Owner View."""

    @classmethod
    def setUpTestData(cls):
        listing_num = 25
        cls.category = Category.objects.create(name='Cat', slug='cat')
        cls.owner = User.objects.create_user(username='Tester')

        for listing in range(listing_num):
            Listing.objects.create(
                category = cls.category,
                user = cls.owner,
                name = f'Listing {listing}',
                slug = f'listing-{listing}',
                description = f'A description for test {listing}.',
                start_bid = listing)

    def setUp(self):
        self.status_code = 200
        self.paginated_by = 20
        self.location = '/my-listings'
        self.context_name = 'users_listings'
        self.template_name = 'auctions/users_listings.html'

        self.client.force_login(self.owner)
        self.resp = self.client.get(reverse('auctions:get_users_listings'))

    def test_view_lists_only_listings_by_desired_user(self):
        for listing in self.resp.context[self.context_name]:
            self.assertEqual(listing.user, self.owner)

    def test_unauthenticated_users_do_not_get_the_page(self):
        self.client.logout()
        resp = self.client.get(self.location)
        self.assertNotEqual(resp.status_code, 200)

class TestDetailedListingView(BaseTestViewMethodsMixin, TestCase):
    """A test case for Detailed Listing View."""

    @classmethod
    def setUpTestData(cls):
        cls.user_owner = User.objects.create_user(username='user_owner')
        cls.user_customer = User.objects.create_user(username='user_customer')
        cls.category = Category.objects.create(name='Cat', slug='cat')
        cls.listing = Listing.objects.create(
            category = cls.category,
            user = cls.user_owner,
            name = 'Listing',
            slug = 'listing',
            description = 'A description for test listing.',
            start_bid = 10.95)
        cls.bid = Bid.objects.create(
            user=cls.user_customer, listing=cls.listing, bid=19.99)

    def setUp(self):
        self.status_code = 200
        self.paginated_by = 20
        self.location = f'/{self.category.slug}/{self.listing.slug}/'
        self.context_name = 'listing'
        self.template_name = 'auctions/listing.html'
        self.resp = self.client.get(reverse(
            'auctions:listing',
            args=[self.category.slug, self.listing.slug]))

        self.basic_context_checklist = (
            'start_bid', 'listing_owner', 'comments'
        )
        self.bid_context_checklist = (
            'current_bid', 'current_bid_owner', 'bid_count'
        )
        self.authenticated_as_customer_checklist = (
            'in_watchlist', 'bid_form', 'comment_form'
        )
        self.authenticated_as_owner_checklist = {
            'shown': 'comment_form', 'hidden': 'bid_form'
        }

    def test_view_context_lists_basic_info(self):
        for context in self.basic_context_checklist:
            self.assertIn(context, self.resp.context)

    def test_bidded_listing_context_lists_bid_info(self):
        for context in self.bid_context_checklist:
            self.assertIn(context, self.resp.context)

    def test_context_for_user_authenticated_as_customer(self):
        self.client.force_login(self.user_customer)
        resp = self.client.get(self.location)
        for context in self.authenticated_as_customer_checklist:
            self.assertIn(context, resp.context)

    def test_owner_context(self):
        self.client.force_login(self.user_owner)
        resp = self.client.get(self.location)
        self.assertIn(self.authenticated_as_owner_checklist['shown'],
            resp.context)
        self.assertNotIn(self.authenticated_as_owner_checklist['hidden'],
            resp.context)

class TestAddListingView(BaseTestViewMethodsMixin, TestCase):
    """A test case for Add Listing View."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Tester')

    def setUp(self):
        self.status_code = 200
        self.template_name = 'auctions/add_listing.html'
        self.location = '/add_listing'
        self.client.force_login(self.user)
        self.resp = self.client.get(reverse('auctions:add_listing'))

    @skip
    def test_context_object_name(self):
        pass

class TestCloseListingView(BaseTestViewMethodsMixin, TestCase):
    """A test case for Close Listing View."""

    @classmethod
    def setUpTestData(cls):
        cls.user_owner = User.objects.create_user(username='user_owner')
        cls.category = Category.objects.create(name='Cat', slug='cat')
        cls.listing = Listing.objects.create(
            category = cls.category,
            user = cls.user_owner,
            name = 'Listing',
            slug = 'listing',
            description = 'A description for test listing.',
            start_bid = 10.95)

    def setUp(self):
        self.status_code = 302
        self.location = f'/{self.category.slug}/{self.listing.slug}/close_listing'
        self.client.force_login(self.user_owner)
        self.resp = self.client.get(reverse('auctions:close_listing',
            args=[self.category.slug, self.listing.slug]))

    @skip
    def test_context_object_name(self):
        pass

    @skip
    def test_view_uses_correct_template(self):
        pass

class TestBiddingView(
        BaseTestViewMethodsMixin, ListingTestViewMethodsMixin, TestCase):
    """A test case for Bidding View."""

    @classmethod
    def setUpTestData(cls):
        listing_num = 50
        cls.owner = User.objects.create_user(username='owner')
        cls.customer = User.objects.create_user(username='customer')
        cls.category = Category.objects.create(name='Cat', slug='cat')

        for listing in range(listing_num):
            Listing.objects.create(
                category = cls.category,
                user = cls.owner,
                name = f'Listing {listing}',
                slug = f'listing-{listing}',
                description = f'A description for test {listing}.',
                start_bid = listing)

        for listing in range(0, listing_num, 2):
            Bid.objects.create(
                user=cls.customer,
                listing=Listing.objects.get(name=f'Listing {listing}'),
                bid=listing + 5)

    def setUp(self):
        self.status_code = 200
        self.paginated_by = 20
        self.location = '/bidding'
        self.context_name = 'bids'
        self.template_name = 'auctions/bidding.html'
        self.client.force_login(self.customer)
        self.resp = self.client.get(reverse('auctions:bidding'))

    @skip
    def test_view_lists_only_active_listings(self):
        pass

    def test_view_lists_only_bids_by_desired_user(self):
        for bid in self.resp.context[self.context_name]:
            self.assertEqual(bid.user, self.customer)

class TestWatchlistView(
        BaseTestViewMethodsMixin, ListingTestViewMethodsMixin, TestCase):
    """A test case for Bidding View."""

    @classmethod
    def setUpTestData(cls):
        listing_num = 50
        cls.owner = User.objects.create_user(username='owner')
        cls.customer = User.objects.create_user(username='customer')
        cls.category = Category.objects.create(name='Cat', slug='cat')

        for listing in range(listing_num):
            Listing.objects.create(
                category = cls.category,
                user = cls.owner,
                name = f'Listing {listing}',
                slug = f'listing-{listing}',
                description = f'A description for test {listing}.',
                start_bid = listing)

        for listing in range(0, listing_num, 2):
            Watchlist.objects.create(user=cls.customer,
                listing=Listing.objects.get(name=f'Listing {listing}'))

    def setUp(self):
        self.status_code = 200
        self.paginated_by = 20
        self.location = '/watchlist'
        self.context_name = 'watchlist'
        self.template_name = 'auctions/watchlist.html'
        self.client.force_login(self.customer)
        self.resp = self.client.get(reverse('auctions:get_watchlist'))

    @skip
    def test_view_lists_only_active_listings(self):
        pass

class TestAddToWatchlist(BaseTestViewMethodsMixin, TestCase):
    """A test case for Add to Watchlist view."""

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username='owner')
        cls.customer = User.objects.create_user(username='customer')
        cls.category = Category.objects.create(name='Cat', slug='cat')

        cls.listing = Listing.objects.create(
            category = cls.category,
            user = cls.owner,
            name = 'Listing 1',
            slug = 'listing-1',
            description = 'A description for test 1.',
            start_bid = 1)

    def setUp(self):
        self.status_code = 302
        self.location = f'/{self.category.slug}/{self.listing.slug}/add_to_watchlist'
        self.client.force_login(self.customer)
        self.resp = self.client.get(reverse('auctions:watch',
            args=[self.category.slug, self.listing.slug]))

    @skip
    def test_context_object_name(self):
        pass

    @skip
    def test_view_uses_correct_template(self):
        pass

    def test_watchlist_creates_object_if_not_watched(self):
        self.assertEqual(len(Watchlist.objects.filter(listing=self.listing)), 1)

    def test_watchlist_deletes_object_if_watched(self):
        self.client.get(reverse('auctions:watch',
            args=[self.category.slug, self.listing.slug]))
        self.assertEqual(len(Watchlist.objects.filter(listing=self.listing)), 0)
