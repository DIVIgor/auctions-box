from xml.etree.ElementInclude import include
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ListingViewSet, UserViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'listings', ListingViewSet)
router.register(r'users', UserViewSet)

app_name = 'API'

urlpatterns = [
    path('', include(router.urls)),
]
