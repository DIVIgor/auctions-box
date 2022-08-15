from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import CategoryViewSet, ListingViewSet, WatchlistViewSet, BidViewSet, CommentViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="Auctions Box API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'listings', ListingViewSet)
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'my-bids', BidViewSet, basename='bids')
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('auth/session/', include('rest_framework.urls')),

    path('docs.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
