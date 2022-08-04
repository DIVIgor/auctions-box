from xml.etree.ElementInclude import include
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ListingViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'listing', ListingViewSet)
router.register(r'comment', CommentViewSet)

app_name = 'API'

urlpatterns = [
    path('', include(router.urls)),
]
