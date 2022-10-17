from django.test import TestCase
from django import forms

from account.models import User
from ..models import Listing, Category
from ..forms import ListingForm, BidForm, CommentForm


class ListingFormTest(TestCase):
    """A test case for a Listing Form."""

    def setUp(self):
        self.form = ListingForm()

    def test_form_field_list_is_correct(self):
        fields = ('category', 'name', 'image', 'start_bid', 'description')
        self.assertTupleEqual(self.form._meta.fields, fields)

    def test_form_field_list_labels_are_correct(self):
        labels = {
            'name': 'Listing name', 'category': 'Category',
            'description': 'Description', 'start_bid': 'Start bid',
            'image': 'Image URL'
        }
        self.assertDictEqual(self.form._meta.labels, labels)

class BidFormTest(TestCase):
    """A test case for a Bid Form."""

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Tester')
        Category.objects.create(name='Test category')
        Listing.objects.create(
            category = Category.objects.get(name='Test category'),
            user = User.objects.get(username='Tester'),
            name = 'Test Listing',
            start_bid = 10.95
        )

    def setUp(self):
        self.form = BidForm()

    def test_form_field_list_is_correct(self):
        fields = ('bid', 'listing')
        self.assertTupleEqual(self.form._meta.fields, fields)

    def test_form_bid_label_is_correct(self):
        self.assertEqual(self.form.fields['bid'].label, 'Your Bid')

    def test_form_listing_widget_is_correct(self):
        widget = type(forms.HiddenInput())
        self.assertEqual(type(self.form._meta.widgets['listing']), widget)

    def test_form_bid_validation_lower_bid(self):
        data = {'listing': Listing.objects.get(id=1), 'bid': 1.25}
        form = BidForm(data)
        self.assertFalse(form.is_valid())

    def test_form_bid_validation_higher_bid(self):
        data = {'listing': Listing.objects.get(id=1), 'bid': 11.25}
        form = BidForm(data)
        self.assertTrue(form.is_valid())

class CommentFormTest(TestCase):
    """A test case for a Comment Form."""

    def setUp(self):
        self.form = CommentForm()

    def test_form_fields_are_correct(self):
        self.assertTupleEqual(self.form._meta.fields, ('text',))

    def test_form_text_label_is_correct(self):
        self.assertEqual(self.form.fields['text'].label, 'Comment')
