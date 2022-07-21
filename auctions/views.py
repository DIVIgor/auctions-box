from copy import copy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify

from django.views.generic import (ListView, DetailView, View, 
    FormView, RedirectView, CreateView)

from .models import Category, Listing, Watchlist
from account.models import User
from .forms import ListingForm, BidForm, CommentForm


class IndexView(ListView):
    model = Listing
    template_name = 'auctions/index.html'
    context_object_name = 'active_listings'

    def get_queryset(self):
        return Listing.objects.filter(is_active=True).order_by('-date_added')


class GetCategories(ListView):
    model = Category
    template_name = 'auctions/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.order_by('name')


class GetListingsByCat(ListView):
    model = Listing
    template_name = 'auctions/listings_by_cat.html'
    context_object_name = 'listings'

    def get_queryset(self):
        return Listing.objects.filter(category__slug=self.kwargs['cat_slug'], is_active=True).order_by('-date_added')

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

        if self.request.user.is_authenticated:
            user_bids = self.object.bid_set.order_by('-date_added')
            if user_bids:
                context['current_bid'] = user_bids[0].bid
                context['current_bid_owner'] = user_bids[0].user

            context['in_watchlist'] = User.objects.get(
                username=self.request.user).watchlist_set.filter(listing=self.object)
            
            context['comment_form'] = self.comment_form_class()

            is_author = self.request.user == context['listing_owner']
            is_last_bidder = False
            if user_bids:
                is_last_bidder =  user_bids[0] == self.request.user
            
            if not is_author and not is_last_bidder and self.object.is_active:
                bid_form = self.bid_form_class()
                context['bid_form'] = bid_form

        return context

    # Needs the form validation improvement
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = {}
        # is_author = request.user == kwargs['listing_owner']

        post_data = copy(self.request.POST)
        post_data['listing'] = self.get_object()
        
        if 'bid_submit' in request.POST: #and not is_author:
            form = self.bid_form_class(post_data)
        elif 'comment_submit' in request.POST:
            form = self.comment_form_class(post_data)

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = self.request.user
            form_data.listing = post_data['listing']
            form_data.save()
            return redirect(post_data['listing'].get_absolute_url())
        elif type(form) == BidForm:
            context['bid_form'] = form
        elif type(form) == CommentForm:
            context['comment_form'] = form
        return self.get_context_data(**context)

class GetUsersListings(ListView):
    model = User
    template_name = 'auctions/users_listings.html'
    context_object_name = 'users_listings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.request.user)
        context['users_listings'] = context['user'].listing_set.order_by('-date_added')
        return context


class GetBidding(ListView):
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
    model = Watchlist
    template_name = 'auctions/watchlist.html'
    context_object_name = 'watchlist'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-date_added')


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
