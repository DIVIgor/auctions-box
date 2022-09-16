from rest_framework.pagination import PageNumberPagination


class BasicPaginationParams(PageNumberPagination):
    """Basic pagination parameters."""

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ListingSetPagination(BasicPaginationParams):
    """Listing set's pagination parameters."""

    pass

class UserSetPagination(BasicPaginationParams):
    """User set's pagination parameters."""

    page_size = 30
    max_page_size = 3000

class BidSetPagination(BasicPaginationParams):
    """Bid set's pagination parameters."""

    page_size = 50
    max_page_size = 5000

class CommentSetPagination(BasicPaginationParams):
    """Comment set's pagination parameters."""

    page_size = 10

class WatchlistPagination(BasicPaginationParams):
    """Watchlist's pagination parameters."""

    page_size = 50
