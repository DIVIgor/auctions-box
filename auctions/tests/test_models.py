from django.test import TestCase

from auctions.models import Category, Listing, Watchlist


class CategoryModelTest(TestCase):
    """A test case for Category model."""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Construction Tools',
        slug='construction-tools')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
