from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from djoser.permissions import CurrentUserOrAdmin

from auctions.models import Category, Listing, Bid, Comment, Watchlist
from .serializers import (CategorySerializer, ListingSerializer,
                          CommentSerializer, BidSerializer,
                          WatchlistSerializer)
from .pagination import (ListingSetPagination, BidSetPagination,
                         CommentSetPagination, WatchlistPagination)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """A read only view set for the `Category` model.
    Data serializer: `CategorySerializer`.

    View set and detail instance.
    Filter listings by category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get',], detail=True,
        url_path='listings')
    def listings(self, request, pk=None):
        """Get listings on the chosen category.
        Data serializer: `ListingSerializer`.
        """

        queryset = Listing.objects.filter(category__pk=pk)
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)

class ListingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """A view set for the `Listing` model.
    Data serializer: `ListingSerializer`.
    Pagination class: `ListingSetPagination`.

    View a set and a detail listing, create and update listings, get comments
    and bids on the chosen listing.

    Permissions:
        - Reading for all users.
        - Creation for all authenticated users
        - Updation and deletions for owners and staff only
    """

    queryset = Listing.objects.order_by('-date_added')
    serializer_class = ListingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ListingSetPagination

    def perform_create(self, serializer):
        """Create a listing.
        Automatic fill `user` and `slug` fields.
        """

        listing_id = self.queryset.filter(category=serializer.validated_data['category']).count() + 1
        title = serializer.validated_data['name']

        serializer.save(
            user=self.request.user,
            slug=slugify(f'{title}_{listing_id}')
        )

    def perform_update(self, serializer):
        """Permission to update for owner and staff only."""

        instance = self.get_object()

        if self.request.user == instance.user or self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied('User is not allowed to modify this listing.')

    @action(methods=['get',], detail=True,
        url_path='comments')
    def comments(self, request, pk=None):
        """Get comments on the chosen listing.
        Data serializer: `CommentSerializer`.
        """

        queryset = Comment.objects.filter(listing__pk=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get',], detail=True,
        url_path='bids')
    def bid(self, request, pk=None):
        """Get bids on the chosen listing.
        Data serializer: `BidSerializer`.
        """

        queryset = Bid.objects.filter(listing__pk=pk)
        serializer = BidSerializer(queryset, many=True)
        return Response(serializer.data)

class WatchlistViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """A view set for the `Watchlist` model.
    Data serializer: `WatchlistSerializer`.
    Pagination class: `WatchlistSetPagination`.

    View set and a single watchlist instance, and delete the instance
    for an owner of the watchlist.
    """

    serializer_class = WatchlistSerializer
    permission_classes = (CurrentUserOrAdmin,)
    pagination_class = WatchlistPagination

    def get_queryset(self):
        """Return a watchlist of the requested user."""

        user = self.request.user
        return Watchlist.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create a watchlist instance if it didn't exist. Otherwise, raise a
        permission denied error.
        """

        if self.get_queryset().filter(listing=serializer.validated_data['listing']):
            raise PermissionDenied('Already in watchlist.')
        serializer.save(user=self.request.user)

class BidViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """A view set for a `Bid` model.
    Data serializer: `BidSerializer`.
    Pagination class: `BidSetPagination`.

    View a set of user's bids, create and delete bids for the user that requests.
    """

    serializer_class = BidSerializer
    permission_classes = (CurrentUserOrAdmin,)
    pagination_class = BidSetPagination

    def get_queryset(self):
        """Return a bid set of the requested user."""

        user = self.request.user
        return Bid.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create a bid instance if a user isn't a listing owner and if a new
        bid is higher than the current one. Otherwise, raise a permission
        denied error.
        """

        listing = serializer.validated_data['listing']
        if listing.user == self.request.user:
            raise PermissionDenied('User cannot bid own listings.')

        queryset = self.get_queryset()
        start_bid = listing.start_bid
        current_bid = max(start_bid,
            queryset.filter(listing=listing).order_by('-bid')[0].bid
                ) if queryset.filter(listing=listing) else start_bid

        if serializer.validated_data['bid'] < current_bid:
            raise PermissionDenied('Wrong bid value.')

        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """A view set for a `Comment` model.
    Data serializer: `CommentSerializer`.
    Pagination class: `CommentSetPagination`.

    View a set of comments, create and delete comments for the chosen listing.

    Permissions:
        - Reading for all users.
        - Creation for all authenticated users
        - Updation and deletions for owners and staff only
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    pagination_class = CommentSetPagination

    def perform_create(self, serializer):
        """Create a comment instance. The `user` field fills automatically."""

        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Permission to update the instance for owner and staff only."""

        instance = self.get_object()

        if self.request.user == instance.user or self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied('User is not allowed to do that.')

    def perform_destroy(self, instance):
        """Permission to delete the instance for owner and staff only."""

        if self.request.user == instance.user or self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied('User is not allowed to do that.')
