from django.test import TestCase

from ..models import Category, Listing, Bid, Comment, Watchlist

from account.models import User


class CategoryModelTest(TestCase):
    """A test case for a Category model."""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category',
        slug='test-category')

    def setUp(self):
        self.category = Category.objects.get(name='Test Category')

    def test_name_label(self):
        field_label = self.category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_slug_label(self):
        field_label = self.category._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_name_max_length(self):
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 80)

    def test_slug_is_unique(self):
        self.assertTrue(self.category._meta.get_field('slug').unique)

    def test_object_name_is_name(self):
        expected_name = self.category.name
        self.assertEqual(str(self.category), expected_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(),
            '/test-category/')

class ListingModelTest(TestCase):
    """A test case for a Listing model."""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category',
        slug='test-category')

        User.objects.create(username='Tester')

        Listing.objects.create(
            category = Category.objects.get(name='Test Category'),
            user = User.objects.get(username='Tester'),
            name = 'Test Listing',
            slug = 'test-listing',
            description = 'A description for test listing.',
            start_bid = 10.95,
            image = 'https://cdn2.iconfinder.com/data/icons/\
                video-game-items-concepts/128/loot-box-512.png',
            is_active = True
        )

    def setUp(self):
        self.listing = Listing.objects.get(name='Test Listing')

    def test_category_foreign_key(self):
        self.assertEqual(self.listing.category.name, 'Test Category')

    def test_user_foreign_key(self):
        self.assertEqual(self.listing.user.username, 'Tester')

    def test_category_label(self):
        self.assertEqual(self.listing._meta.get_field('category')\
            .verbose_name, 'category')

    def test_user_label(self):
        self.assertEqual(self.listing._meta.get_field('user').verbose_name,
            'user')

    def test_name_label(self):
        field_label = self.listing._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_slug_label(self):
        field_label = self.listing._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_description_label(self):
        field_label = self.listing._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_start_bid_label(self):
        field_label = self.listing._meta.get_field('start_bid').verbose_name
        self.assertEqual(field_label, 'start bid')

    def test_image_label(self):
        field_label = self.listing._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

    def test_is_active_label(self):
        field_label = self.listing._meta.get_field('is_active').verbose_name
        self.assertEqual(field_label, 'is active')

    def test_date_added_label(self):
        self.assertEqual(self.listing._meta.get_field('date_added')\
            .verbose_name, 'date added')

    def test_date_updated_label(self):
        self.assertEqual(self.listing._meta.get_field('date_updated')\
            .verbose_name, 'date updated')

    def test_name_max_length(self):
        max_length = self.listing._meta.get_field('name').max_length
        self.assertEqual(max_length, 250)

    def test_slug_max_length(self):
        max_length = self.listing._meta.get_field('slug').max_length
        self.assertEqual(max_length, 250)

    def test_start_bid_max_digits(self):
        max_digits = self.listing._meta.get_field('start_bid').max_digits
        self.assertEqual(max_digits, 9)

    def test_start_bid_decimal_places(self):
        decimal_places = self.listing._meta.get_field('start_bid')\
            .decimal_places
        self.assertEqual(decimal_places, 2)

    def test_slug_is_unique(self):
        self.assertTrue(self.listing._meta.get_field('slug').unique)

    def test_image_can_be_blank(self):
        self.assertTrue(self.listing._meta.get_field('image').blank)

    def test_date_added_auto_now_add(self):
        self.assertTrue(self.listing._meta.get_field('date_added')\
            .auto_now_add)

    def test_date_updated_auto_now(self):
        self.assertTrue(self.listing._meta.get_field('date_updated').auto_now)

    def test_obj_name_is_name(self):
        self.assertEqual(self.listing.name, str(self.listing))

    def test_absolute_url(self):
        self.assertEqual(self.listing.get_absolute_url(),
            '/test-category/test-listing/')

class BidModelTest(TestCase):
    """A test case for a Bid model."""

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Owner')
        User.objects.create(username='Tester')

        Category.objects.create(name='Test Category')

        Listing.objects.create(
            category = Category.objects.get(name='Test Category'),
            user = User.objects.get(username='Owner'),
            name = 'Test Listing',
            start_bid = 10.95
        )

        Bid.objects.create(
            user = User.objects.get(username='Tester'),
            listing = Listing.objects.get(name='Test Listing'),
            bid = 11.5
        )

    def setUp(self):
        self.bid = Bid.objects.get(id=1)

    def test_user_foreign_key(self):
        self.assertEqual(self.bid.user.username, 'Tester')

    def test_listing_foreign_key(self):
        self.assertEqual(self.bid.listing.name, 'Test Listing')

    def test_bid_label(self):
        self.assertEqual(self.bid._meta.get_field('bid').verbose_name, 'bid')

    def test_bid_max_digits(self):
        self.assertEqual(self.bid._meta.get_field('bid').max_digits, 19)

    def test_bid_decimal_places(self):
        self.assertEqual(self.bid._meta.get_field('bid').decimal_places, 2)

    def test_date_added_auto_now_add(self):
        self.assertTrue(self.bid._meta.get_field('date_added')\
            .auto_now_add)

    def test_date_updated_auto_now(self):
        self.assertTrue(self.bid._meta.get_field('date_updated').auto_now)

class CommentModelTest(TestCase):
    """A test case for a Comment model."""

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Tester')

        Category.objects.create(name='Test Category')

        Listing.objects.create(
            category = Category.objects.get(name='Test Category'),
            user = User.objects.get(username='Tester'),
            name = 'Test Listing',
            start_bid = 10.95
        )

        Comment.objects.create(
            user = User.objects.get(username='Tester'),
            listing = Listing.objects.get(name='Test Listing'),
            text = """Ipsum cillum esse proident irure ea tempor duis.
                Irure veniam consectetur magna ullamco minim ut sint. Eu
                cupidatat elit incididunt est est proident proident ullamco.
                Dolor Lorem dolore quis officia ut occaecat est anim do sit.
                Laborum et officia enim id ex consectetur.
            """
        )

    def setUp(self):
        self.comment = Comment.objects.get(id=1)

    def test_user_foreign_key(self):
        self.assertEqual(self.comment.user.username, 'Tester')

    def test_listing_foreign_key(self):
        self.assertEqual(self.comment.listing.name, 'Test Listing')

    def test_user_label(self):
        self.assertEqual(self.comment._meta.get_field('user').verbose_name,
            'user')

    def test_listing_label(self):
        self.assertEqual(self.comment._meta.get_field('listing').verbose_name,
            'listing')

    def test_text_label(self):
        self.assertEqual(self.comment._meta.get_field('text').verbose_name,
            'text')

    def test_date_added_label(self):
        self.assertEqual(self.comment._meta.get_field('date_added')\
            .verbose_name, 'date added')

    def test_date_updated_label(self):
        self.assertEqual(self.comment._meta.get_field('date_updated')\
            .verbose_name, 'date updated')

    def test_text_max_length(self):
        self.assertEqual(self.comment._meta.get_field('text').max_length,
            3000)

    def test_date_added_auto_now_add(self):
        self.assertTrue(self.comment._meta.get_field('date_added')\
            .auto_now_add)

    def test_date_updated_auto_now(self):
        self.assertTrue(self.comment._meta.get_field('date_updated').auto_now)

class TestWatchlistModel(TestCase):
    """A test case for a Watchlist model."""
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Tester')

        Category.objects.create(name='Test Category')

        Listing.objects.create(
            category = Category.objects.get(name='Test Category'),
            user = User.objects.get(username='Tester'),
            name = 'Test Listing',
            start_bid = 10.95
        )

        Watchlist.objects.create(
            user = User.objects.get(username='Tester'),
            listing = Listing.objects.get(name='Test Listing')
        )

    def setUp(self):
        self.watchlist = Watchlist.objects.get(id=1)

    def test_user_foreign_key(self):
        self.assertEqual(self.watchlist.user.username, 'Tester')

    def test_listing_foreign_key(self):
        self.assertEqual(self.watchlist.listing.name, 'Test Listing')

    def test_user_label(self):
        self.assertEqual(self.watchlist._meta.get_field('user').verbose_name,
            'user')

    def test_listing_label(self):
        self.assertEqual(self.watchlist._meta.get_field('listing').verbose_name,
            'listing')

    def test_date_added_label(self):
        self.assertEqual(self.watchlist._meta.get_field('date_added')\
            .verbose_name, 'date added')

    def test_date_updated_label(self):
        self.assertEqual(self.watchlist._meta.get_field('date_updated')\
            .verbose_name, 'date updated')

    def test_date_added_auto_now_add(self):
        self.assertTrue(self.watchlist._meta.get_field('date_added')\
            .auto_now_add)

    def test_date_updated_auto_now(self):
        self.assertTrue(self.watchlist._meta.get_field('date_updated')\
            .auto_now)
