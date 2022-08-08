from rest_framework import serializers

from account.models import User
from auctions.models import Category, Listing, Bid, Comment, Watchlist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('id', 'category', 'user', 'name', 'description', 'image',
            'start_bid', 'date_added', 'date_updated')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'
