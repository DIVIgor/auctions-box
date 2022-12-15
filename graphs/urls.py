from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import CategoryAnalyticsView


app_name = 'graphs'

urlpatterns = [
    path('', login_required(CategoryAnalyticsView.as_view()), name='cat_graph'),
]
