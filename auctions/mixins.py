from django.db.models.functions import Greatest
from django.db.models import F, Q
from django.db.models import Max

from .models import Listing


class GetListingsQuerySetMixin:
    """Mixin for classes that use listing query sets.
    Unificates a `get_queryset` function.
    """

    lst_orderings = {
    'date_desc': '-date_added', 'date_asc': 'date_added',
    'name': 'name', 'bid_desc': '-current_bid',
    'bid_asc': 'current_bid'
}

    def filter_listings(self, query):
        """Filter and order a query by request."""

        bid_filter = self.request.GET.get('bid_filter')
        lst_ordering = self.request.GET.get('lst_sort')

        if bid_filter == 'all':
            pass
        elif bid_filter == 'no_bids':
            query = query.filter(max_bid=None)
        elif bid_filter == 'bids':
            query = query.filter(Q(current_bid=F('max_bid')))

        if lst_ordering:
            query = query.order_by(self.lst_orderings[lst_ordering])

        return query

    def get_listingset(self):
        """Get a query set of listings annotated by `max_bid` and
        `current_bid` ordered by descending `date_added`.
        Call the `filter_listings` function.
        """

        query = Listing.objects.annotate(
            max_bid=Max('bid__bid'), current_bid=Greatest('start_bid', 'max_bid')
        ).order_by('-date_added')
        query = self.filter_listings(query)

        return query
