from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ListingViewSet, WatchlistViewSet, BidViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'listings', ListingViewSet)
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'my-bids', BidViewSet, basename='bids')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('auth/session/', include('rest_framework.urls')),
]
