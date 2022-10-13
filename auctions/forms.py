from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Listing, Bid, Comment


class ListingForm(forms.ModelForm):
    """A listing form.
    Contains fields: `category`, `name`, `image`, `start_bid`,
    and `description`.
    """

    class Meta:
        model = Listing
        fields = [
            'category', 'name',
            'image', 'start_bid',
            'description'
        ]
        labels = {
            'name': 'Listing name', 'category': 'Category',
            'description': 'Description', 'start_bid': 'Start bid',
            'image': 'Image URL'
        }

class BidForm(forms.ModelForm):
    """A bid form.
    Contains fields: `bid`, `listing`.
    """

    class Meta:
        model = Bid
        fields = ('bid', 'listing')
        labels = {'bid': 'Your Bid'}
        widgets = {'listing': forms.HiddenInput()}

    def clean(self):
        """Validate a new bid."""

        new_bid = self.cleaned_data.get('bid')
        listing = self.cleaned_data.get('listing')
        start_bid = listing.start_bid
        bids = listing.bid_set.order_by('-date_added')
        current_bid = bids[0].bid if bids else start_bid

        if new_bid <= current_bid:
            self._errors['bid'] = self.error_class([
                'Bid must be higher than current.'])
            raise ValidationError(
                _('Invalid value: %(value)s'),
                code='invalid',
                params={'value': new_bid},
            )
        return self.cleaned_data

class CommentForm(forms.ModelForm):
    """A comment form.
    Contains field `text`.
    """

    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Comment'}