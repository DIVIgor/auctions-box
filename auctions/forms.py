from django import forms

from .models import Listing, Bid, Comment


class ListingForm(forms.ModelForm):
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
    class Meta:
        model = Bid
        fields = ('bid', 'listing')
        labels = {'bid': 'Your Bid'}
        widgets = {'listing': forms.HiddenInput()}

    def clean(self):
        new_bid = self.cleaned_data.get('bid')
        listing = self.cleaned_data.get('listing')
        start_bid = listing.start_bid
        bids = listing.bid_set.order_by('-date_added')
        current_bid = bids[0].bid if bids else start_bid

        if new_bid <= current_bid:
            raise forms.ValidationError(
                "Your bid must be higher than previous"
            )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Comment'}