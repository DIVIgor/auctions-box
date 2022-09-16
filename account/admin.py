from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """A user class for admin panel.
    Displays user's info: `id`, `username`, `email`, `is_staff`, `is_active`,
    `last_login`, `date_joined`.
    Set filters: `is_active`, `is_staff`, `last_login`, `date_joined`.
    Search fields: `username`, `email`.
    """

    list_display = (
        'id', 'username', 'email',
        'is_staff', 'is_active', 'last_login',
        'date_joined'
    )
    list_display_links = list_display
    list_filter = (
        'is_active', 'is_staff',
        'last_login', 'date_joined'
    )
    search_fields = ('username', 'email')