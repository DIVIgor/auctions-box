from rest_framework.pagination import PageNumberPagination


class BasicPaginationParams(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ListingSetPagination(BasicPaginationParams):
    pass

class UserSetPagination(BasicPaginationParams):
    page_size = 30
    max_page_size = 3000

class BidSetPagination(BasicPaginationParams):
    page_size = 50
    max_page_size = 5000

class CommentSetPagination(BasicPaginationParams):
    page_size = 10

class WatchlistPagination(BasicPaginationParams):
    page_size = 50