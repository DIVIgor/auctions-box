from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from account.models import User
from auctions.models import Category, Listing, Bid, Comment, Watchlist
from .serializers import CategorySerializer, ListingSerializer, CommentSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # @action(methods=['get', 'post'], detail=False)
    # def listing(self, request, pk=None):
    #     listings = Listing.objects.filter(category=pk)
    #     return Response({'listings': listings[:]})

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = Listing.objects.filter(category__slug=slug)
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(listing__id=None)
    serializer_class = CommentSerializer