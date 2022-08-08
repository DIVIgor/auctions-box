from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from account.models import User
from auctions.models import Category, Listing, Bid, Comment, Watchlist
from .serializers import (UserSerializer, CategorySerializer, ListingSerializer,
    CommentSerializer, BidSerializer, WatchlistSerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get', 'post', 'put', 'patch'], detail=True,
        url_path='listings')
    def listings(self, request, pk=None):
        queryset = Listing.objects.filter(category__pk=pk)
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    # lookup_field = 'slug'

    # def retrieve(self, request, pk=None):
    #     queryset = Listing.objects.filter(category__id=pk)
    #     serializer = ListingSerializer(queryset, many=True)
    #     return Response(serializer.data)

    @action(methods=['get', 'post'], detail=True,
        url_path='comments')
    def comments(self, request, id=None):
        queryset = Comment.objects.filter(listing__id=id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=True,
        url_path='bids')
    def bid(self, request, id=None):
        queryset = Bid.objects.filter(listing__id=id)
        serializer = BidSerializer(queryset, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(methods=['get', 'post', 'put', 'patch'], detail=True,
        url_path='watchlist')
    def watchlist(self, request, username=None):
        queryset = Watchlist.objects.filter(user__username=username)
        serializer = WatchlistSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True,
        url_path='bids')
    def bid(self, request, username=None):
        queryset = Bid.objects.filter(user__username=username)
        serializer = BidSerializer(queryset, many=True)
        return Response(serializer.data)
