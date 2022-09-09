from copy import copy

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.db.models.functions import Greatest
from django.db.models import F, Q
from django.db.models import Max
from django.contrib.postgres.search import SearchVector
from django.views.generic import (ListView, DetailView, View,
    FormView, RedirectView, CreateView)

from .models import Category, Listing, Watchlist
from account.models import User
from .forms import ListingForm, BidForm, CommentForm


class IndexView(ListView):
    paginate_by = 15
    model = Listing
    template_name = 'auctions/index.html'
    context_object_name = 'active_listings'

    def get_queryset(self):
        # bid_filters = {'all': '', 'bids': '', 'no_bids': ''}
        lst_orderings = {'date_desc': '-date_added', 'date_asc': 'date_added',
            'name': 'name', 'bid_desc': '-current_bid', 'bid_asc': 'current_bid'}
        bid_filter = self.request.GET.get('bid_filter')
        lst_ordering = self.request.GET.get('lst_sort')

        query = self.model.objects.filter(is_active=True).annotate(
            max_bid=Max('bid__bid'), current_bid=Greatest('start_bid', 'max_bid'))
        if bid_filter == 'all':
            pass
        elif bid_filter == 'no_bids':
            query = query.filter(max_bid=None)
        elif bid_filter == 'bids':
            query = query.filter(Q(current_bid=F('max_bid')))
        
        if lst_ordering:
            query = query.order_by(lst_orderings[lst_ordering])
        # Listing.objects.annotate()
        return query
        # return .filter(fltr).order_by(
        #         *ordr if type(ordr)==tuple else ordr)


class SearchView(IndexView):
    template_name = 'auctions/listing_search.html'
    context_object_name = 'listing_search'
    model = Listing

    def get_queryset(self):
        search_request = self.request.GET.get('q')
        if search_request:
            # query = self.model.objects.annotate(
            #     similarity=TrigramWordSimilarity(search_request,
            #     'name')
            # ).filter(similarity__gt=0.3).order_by('-similarity')
            query = self.model.objects.annotate(search=SearchVector('name', 'description', 'user__username')
            ).filter(search=search_request)
        else:
            query = self.model.objects.all()
        return query
    

class GetCategories(ListView):
    model = Category
    template_name = 'auctions/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return self.model.objects.all()


class GetListingsByCat(ListView):
    paginate_by = 15
    model = Listing
    template_name = 'auctions/listings_by_cat.html'
    context_object_name = 'listings'

    def get_queryset(self):
        return self.model.objects.filter(category__slug=self.kwargs['cat_slug'],\
            is_active=True).order_by('-date_added').annotate(current_bid=Max('bid__bid'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return context


class GetListing(DetailView, View):
    model = Listing
    bid_form_class = BidForm
    comment_form_class = CommentForm
    template_name = 'auctions/listing.html'
    slug_url_kwarg = 'listing_slug'
    context_object_name = 'listing'

    # def get_queryset(self):
    #     return get_object_or_404(Listing, slug=self.kwargs['listing_slug'])

    def get_context_data(self, **kwargs):
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
        elif type(form) == BidForm and not form.is_valid():
            context['bid_form'] = form
        elif type(form) == CommentForm and not form.is_valid():
            context['comment_form'] = form
        print(self.get_context_data(**context))
        return self.render_to_response(self.get_context_data(**context))


class GetUsersListings(ListView):
    paginate_by = 20
    model = User
    template_name = 'auctions/users_listings.html'
    context_object_name = 'users_listings'

    def get_queryset(self):
        return Listing.objects.filter(user=get_object_or_404(User, \
            username=self.request.user)).order_by('-date_added')\
            .annotate(current_bid=Max('bid__bid'))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user'] = get_object_or_404(User, username=self.request.user)
    #     context['users_listings'] = context['user'].listing_set.order_by('-date_added')
    #     return context


class GetBidding(ListView):
    paginate_by = 20
    model = User
    template_name = 'auctions/bidding.html'
    # context_object_name = 'bids'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.request.user)
        context['bids'] = context['user'].bid_set.order_by('-date_added')
        return context


class AddListing(FormView):
    form_class = ListingForm
    template_name = 'auctions/add_listing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing_form'] = context['form']
        return context

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.user = self.request.user
        listing_id = Listing.objects.filter(category=listing.category).count() + 1
        listing.slug = slugify(f'{listing.name}_{listing_id}')
        listing.save()
        return redirect(listing.get_absolute_url())


class GetWatchlist(ListView):
    paginate_by = 20
    model = Watchlist
    template_name = 'auctions/watchlist.html'
    context_object_name = 'watchlist'

    def get_queryset(self):
        return Listing.objects.filter(watchlist__user=get_object_or_404(User, username=self.request.user)).order_by('-date_added')\
            .annotate(current_bid=Max('bid__bid'))
        # return self.model.objects.filter(user=self.request.user).order_by('-date_added')\
        #     .annotate(current_bid=Max('bid__bid'))


class AddToWatchlist(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'watch'

    def get_redirect_url(self, *args, **kwargs):
        listing = get_object_or_404(Listing, slug=kwargs['listing_slug'])
        if self.request.user != listing.user:
            watchlist, created = Watchlist.objects.get_or_create(user=self.request.user,
                listing=listing)
            if not created:
                watchlist.delete()
        return listing.get_absolute_url()


class CloseListing(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'close_listing'
    
    def get_redirect_url(self, *args, **kwargs):
        listing = get_object_or_404(Listing, slug=kwargs['listing_slug'])
        if listing.user == self.request.user:
            listing.is_active = False
            listing.save()
        return listing.get_absolute_url()
