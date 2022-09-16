from rest_framework import serializers

from auctions.models import Category, Listing, Bid, Comment, Watchlist


class CategorySerializer(serializers.ModelSerializer):
    """A category data serializer.
    Fields: `id`, `name`.
    """

    class Meta:
        model = Category
        fields = ('id', 'name')

class ListingSerializer(serializers.ModelSerializer):
    """A listing data serializer.
    Fields: `id`, `category`, `user`, `name`, `description`, `image`,
    `start_bid`, `date_added`, `date_updated`.
    Read only fields: `id`, `user`, `date_added`, `date_updated`.
    """

    class Meta:
        model = Listing
        fields = ('id', 'category', 'user', 'name', 'description', 'image',
            'start_bid', 'date_added', 'date_updated')
        read_only_fields = ('id', 'user', 'date_added', 'date_updated')

class CommentSerializer(serializers.ModelSerializer):
    """A comment data serializer.
    Contains all fields.
    Read only `user` field.
    """

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)

class BidSerializer(serializers.ModelSerializer):
    """A bid data serializer.
    Contains all fields.
    Read only `user` field.
    """

    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ('user',)

class WatchlistSerializer(serializers.ModelSerializer):
    """A watchlist data serializer.
    Contains all fields.
    Read only `user` field.
    """

    class Meta:
        model = Watchlist
        fields = '__all__'
        read_only_fields = ('user',)
