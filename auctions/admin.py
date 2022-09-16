from django.contrib import admin

from .models import Category, Listing, Bid, Comment, Watchlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """A category class for admin panel.
    Displays category's info: `id`, `name`.
    Prepopulated fields: `slug` by category name.
    Search fields: `name`.
    """

    list_display = ('id', 'name')
    list_display_links = list_display
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """A listing class for admin panel.
    Displays listing's info: `id`, `name`, `category`, `user`, `is_active`,
    `date_added`, `date_updated`.
    Editable fields: `is_active`.
    Set filters: `category`, `user`, `is_active`, `date_added`, `date_updated`.
    Prepopulated fields: `slug` by listing name.
    Search fields: `name`, `category__name`, `user__username`.
    """

    list_display = (
        'id', 'name', 'category',
        'user', 'is_active', 'date_added',
        'date_updated'
    )
    list_editable = ('is_active',)
    list_display_links = list_display[:4]
    list_filter = (
        'category', 'user',
        'is_active', 'date_added', 'date_updated'
    )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name', 'user__username')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """A bid class for admin panel.
    Displays bid's info: `id`, `listing`, `user`, `bid`.
    Set filters: `listing`, `user`, `bid`.
    Search fields: `listing__name`, `user__username`, `bid`.
    """

    list_display = ('id', 'listing', 'user', 'bid')
    list_display_links = list_display
    list_filter = ('listing', 'user', 'bid')
    search_fields = ('listing__name', 'user__username', 'bid')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """A comment class for admin panel.
    Displays comment's info: `id`, `listing`, `user`, `date_added`.
    Set filters: `id`, `listing`, `user`, `date_added`.
    Search fields: `listing__name`, `user__username`.
    """

    list_display = ('id', 'listing', 'user', 'date_added')
    list_display_links = list_display
    list_filter = ('id', 'listing', 'user', 'date_added')
    search_fields = ('listing__name', 'user__username')

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    """A watchlist class for admin panel.
    Displays watchlist's info: `id`, `user`, `listing`.
    Set filters: `user`, `listing`.
    Search fields: `user__username`, `listing__name`.
    """

    list_display = ('id', 'user', 'listing')
    list_display_links = list_display
    list_filter = ('user', 'listing')
    search_fields = ('user__username', 'listing__name')