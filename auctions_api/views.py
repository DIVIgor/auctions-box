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
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get',], detail=True,
        url_path='listings')
    def listings(self, request, pk=None):
        queryset = Listing.objects.filter(category__pk=pk)
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)

class ListingViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ListingSetPagination

    def perform_create(self, serializer):
        listing_id = self.queryset.filter(category=serializer.validated_data['category']).count() + 1
        title = serializer.validated_data['name']

        serializer.save(
            user=self.request.user,
            slug=slugify(f'{title}_{listing_id}')
        )

    def perform_update(self, serializer):
        """Permissions to update for owner and staff"""
        instance = self.get_object()

        if self.request.user == instance.user or self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied('User is not allowed to modify this listing.')

    @action(methods=['get',], detail=True,
        url_path='comments')
    def comments(self, request, pk=None):
        queryset = Comment.objects.filter(listing__pk=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get',], detail=True,
        url_path='bids')
    def bid(self, request, pk=None):
        queryset = Bid.objects.filter(listing__pk=pk)
        serializer = BidSerializer(queryset, many=True)
        return Response(serializer.data)

class WatchlistViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = (CurrentUserOrAdmin,)
    pagination_class = WatchlistPagination

    def get_queryset(self):
        user = self.request.user
        return Watchlist.objects.filter(user=user)

    def perform_create(self, serializer):
        if self.get_queryset().filter(listing=serializer.validated_data['listing']):
            raise PermissionDenied('Already in watchlist.')
        serializer.save(user=self.request.user)
    
class BidViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = BidSerializer
    permission_classes = (CurrentUserOrAdmin,)
    pagination_class = BidSetPagination

    def get_queryset(self):
        user = self.request.user
        return Bid.objects.filter(user=user)

    def perform_create(self, serializer):
        listing = serializer.validated_data['listing']
        if listing.user == self.request.user:
            raise PermissionDenied('User cannot bid own listings.')

        queryset = self.get_queryset()
        start_bid = listing.start_bid
        current_bid = max(start_bid, queryset.filter(listing=listing).order_by\
            ('-bid')[0].bid) if queryset.filter(listing=listing) else start_bid

        if serializer.validated_data['bid'] < current_bid:
            raise PermissionDenied('Wrong bid value.')


        # Raw query (An issue with results. pgAdmin returns the correct value
        # while django on server and in shell - wrong)
        # current_bid = Bid.objects.raw(f"""
        #     SELECT id, (SELECT MAX(bids)
        #         FROM (VALUES (start_bid), (users_maxbid)) AS listing_bids(bids)) AS curr_bid
        #     FROM auctions_listing
        #     JOIN (
        #         SELECT listing_id, MAX(bid) AS users_maxbid
        #         FROM auctions_bid
        #         WHERE user_id={self.request.user.id} AND listing_id={listing.id}
        #         GROUP BY listing_id, user_id
        #     ) AS maxbid ON auctions_listing.id = maxbid.listing_id
        #     WHERE auctions_listing.id={listing.id}
        # """)

        # if serializer.validated_data['bid'] < current_bid[0].bid:
        #     raise PermissionDenied('Wrong bid value.')

        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    pagination_class = CommentSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        instance = self.get_object()

        if self.request.user == instance.user or self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied('User is not allowed to do that.')

    def perform_destroy(self, instance):
        if self.request.user == instance.user or self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied('User is not allowed to do that.')
