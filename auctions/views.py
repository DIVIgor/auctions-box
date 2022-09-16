from copy import copy

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.db.models.functions import Greatest
from django.db.models import F, Q
from django.db.models import Max
from django.contrib.postgres.search import SearchVector
from django.views.generic import (ListView, DetailView, View,
    FormView, RedirectView)

from account.models import User
from .models import Category, Listing, Watchlist
from .forms import ListingForm, BidForm, CommentForm


LST_ORDERINGS = {
    'date_desc': '-date_added', 'date_asc': 'date_added',
    'name': 'name', 'bid_desc': '-current_bid',
    'bid_asc': 'current_bid'
}

def filter_listings(self, query):
    """A function that filters and orders a query by request."""

    bid_filter = self.request.GET.get('bid_filter')
    lst_ordering = self.request.GET.get('lst_sort')

    if bid_filter == 'all':
        pass
    elif bid_filter == 'no_bids':
        query = query.filter(max_bid=None)
    elif bid_filter == 'bids':
        query = query.filter(Q(current_bid=F('max_bid')))

    if lst_ordering:
        query = query.order_by(LST_ORDERINGS[lst_ordering])

    return query


class IndexView(ListView):
    """Render the homepage, set by a number of listings per page and
    template name.
    """

    paginate_by = 15
    model = Listing
    template_name = 'auctions/index.html'
    context_object_name = 'active_listings'

    def get_queryset(self):
        """Return a set of listings with extra data: `max_bid` and
        `current_bid`. Ordering by date added descending by default.
        """

        query = self.model.objects.filter(is_active=True).annotate(
            max_bid=Max('bid__bid'), current_bid=Greatest('start_bid', 'max_bid')
        ).order_by('-date_added')
        query = filter_listings(self, query)

        return query


class SearchView(IndexView):
    """Render page that depends on user's request."""

    template_name = 'auctions/listing_search.html'
    context_object_name = 'listing_search'
    model = Listing

    def get_queryset(self):
        """Return a query annotated by `current_bid` - starting bid or
        user's one, `max_bid` - the max set bid or none, and `search`
        - fields to look in. If set, filter the query by a search request.
        """

        search_request = self.request.GET.get('q')
        query = self.model.objects.annotate(max_bid=Max('bid__bid'),
            current_bid=Greatest('start_bid', 'max_bid'),
            search=SearchVector('name', 'description', 'user__username')
        ).order_by('-date_added')
        if search_request:
            query = query.filter(search=search_request)

        query = filter_listings(self, query)
        return query


class GetCategories(ListView):
    """Render a list of categories."""

    model = Category
    template_name = 'auctions/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """Return a queryset of categories."""

        return self.model.objects.all()


class GetListingsByCat(ListView):
    """Render listings by chosen category."""

    paginate_by = 15
    model = Listing
    template_name = 'auctions/listings_by_cat.html'
    context_object_name = 'listings'

    def get_queryset(self):
        """Return a set of listings by category with extra data: `max_bid` and
        `current_bid`. Ordering by date added descending by default.
        """
        query = self.model.objects.filter(category__slug=self.kwargs['cat_slug'],
            is_active=True).annotate(max_bid=Max('bid__bid'),
                current_bid=Greatest('start_bid', 'max_bid'),
                search=SearchVector('name', 'description', 'user__username')
        ).order_by('-date_added')

        query = filter_listings(self, query)
        return query

    def get_context_data(self, **kwargs):
        """Return context by category."""
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return context


class GetListing(DetailView, View):
    """Render a detailed listing page with a bid and a comment forms."""

    model = Listing
    bid_form_class = BidForm
    comment_form_class = CommentForm
    template_name = 'auctions/listing.html'
    slug_url_kwarg = 'listing_slug'
    context_object_name = 'listing'


    def get_context_data(self, **kwargs):
        """Collect and return a context. Contains:
        Extra data: `cat_slug`,
        `comments`, `current_bid`, `current_bid_owner`, `bid_count`,
        `in_watchlist`.
        Forms: `comment_form`, `bid_form`.
        """

        context = super().get_context_data(**kwargs)
        context['cat_slug'] = self.kwargs['cat_slug']
        context['listing_slug'] = self.kwargs['listing_slug']
        context['start_bid'] = self.object.start_bid
        context['listing_owner'] = self.object.user
        context['comments'] = self.object.comment_set.order_by('-date_added')

        bids = self.object.bid_set.order_by('-bid')
        if bids:
            context['current_bid'] = bids[0].bid
            context['current_bid_owner'] = bids[0].user
            context['bid_count'] = len(bids)

        if self.request.user.is_authenticated:
            context['in_watchlist'] = User.objects.get(
                username=self.request.user).watchlist_set.filter(listing=self.object)

            context['comment_form'] = self.comment_form_class()

            is_author = self.request.user == context['listing_owner']
            is_last_bidder = False
            if bids:
                is_last_bidder =  bids[0] == self.request.user

            if not is_author and not is_last_bidder and self.object.is_active:
                bid_form = self.bid_form_class()
                context['bid_form'] = bid_form

        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Check `POST` request for type of submit. Depends on request
        build a filled form for bid or comment. Redirect to the listing page if
        form is valid. Otherwise append invalid data to context and rerender
        the page.
        """

        self.object = self.get_object()
        context = {}
        post_data = copy(self.request.POST)
        post_data['listing'] = self.object

        if 'bid_submit' in request.POST:
            form = self.bid_form_class(post_data)
        elif 'comment_submit' in request.POST:
            form = self.comment_form_class(post_data)

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = self.request.user
            form_data.listing = self.object
            form_data.save()
            return redirect(self.object.get_absolute_url())
        elif isinstance(form, BidForm) and not form.is_valid():
            context['bid_form'] = form
        elif isinstance(form, CommentForm) and not form.is_valid():
            context['comment_form'] = form
        return self.render_to_response(self.get_context_data(**context))


class GetUsersListings(ListView):
    """Render listings created by a user."""

    paginate_by = 20
    model = Listing
    template_name = 'auctions/users_listings.html'
    context_object_name = 'users_listings'

    def get_queryset(self):
        """Return queryset of listings created by a user."""

        query = self.model.objects.filter(user=get_object_or_404(
            User, username=self.request.user)).order_by(
                '-date_added').annotate(max_bid=Max('bid__bid'),
                    current_bid=Greatest('start_bid', 'max_bid'),
                    search=SearchVector('name', 'description', 'user__username'))

        query = filter_listings(self, query)
        return query


class GetBidding(ListView):
    """Render list of bids made by a user."""

    paginate_by = 20
    model = User
    template_name = 'auctions/bidding.html'

    def get_context_data(self, **kwargs):
        """Return context by user."""

        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.request.user)
        context['bids'] = context['user'].bid_set.order_by('-date_added')
        return context


class AddListing(FormView):
    """Render a page with a create listing form."""

    form_class = ListingForm
    template_name = 'auctions/add_listing.html'

    def get_context_data(self, **kwargs):
        """Return form context."""

        context = super().get_context_data(**kwargs)
        context['listing_form'] = context['form']
        return context

    def form_valid(self, form):
        """Fill user and slug fields of the validated form and save it.
        Redirect to just created listing page.
        """

        listing = form.save(commit=False)
        listing.user = self.request.user
        listing_id = Listing.objects.filter(category=listing.category).count() + 1
        listing.slug = slugify(f'{listing.name}_{listing_id}')
        listing.save()
        return redirect(listing.get_absolute_url())


class GetWatchlist(ListView):
    """Render user's watchlist watchlist."""

    paginate_by = 20
    model = Watchlist
    template_name = 'auctions/watchlist.html'
    context_object_name = 'watchlist'

    def get_queryset(self):
        """Return query of listings watched by a user."""

        query = Listing.objects.filter(watchlist__user=get_object_or_404(User,
            username=self.request.user)).annotate(max_bid=Max('bid__bid'),
                current_bid=Greatest('start_bid', 'max_bid'),
                search=SearchVector('name', 'description', 'user__username')
        ).order_by('-date_added')

        query = filter_listings(self, query)

        return query


class AddToWatchlist(RedirectView):
    """Add a listing to a user's watchlist."""

    permanent = False
    query_string = True
    pattern_name = 'watch'
    model = Watchlist

    def watch_or_unwatch(self, listing):
        """Add a listing to the watchlist or delete from it."""

        if self.request.user != listing.user:
            watchlist, created = self.model.objects.get_or_create(
                user=self.request.user, listing=listing)
            if not created:
                watchlist.delete()

    def get_redirect_url(self, *args, **kwargs):
        """Get a listing by a slug. Call `watch_or_unwatch` function. Redirect
        to just watched/unwatched listing page.
        """

        listing = get_object_or_404(Listing, slug=kwargs['listing_slug'])
        self.watch_or_unwatch(listing)

        return listing.get_absolute_url()


class CloseListing(RedirectView):
    """Close a listing."""

    permanent = False
    query_string = True
    pattern_name = 'close_listing'

    def deactivate_listing(self, listing):
        """Set `is_active` parameter to `False` for the listing. Return
        the listing.
        """

        if listing.user == self.request.user:
            listing.is_active = False
            listing.save()
        return listing

    def get_redirect_url(self, *args, **kwargs):
        """Get a listing by a slug. Call `deactivate_liting` function.
        Redirect to a listing page.
        """

        listing = get_object_or_404(Listing, slug=kwargs['listing_slug'])
        listing = self.deactivate_listing(listing)

        return listing.get_absolute_url()
