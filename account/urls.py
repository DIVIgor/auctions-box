from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import login_view, logout_view, register
from .views import UserView, ChangePassView


app_name = 'account'

urlpatterns = [
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),
    path('details', login_required(UserView.as_view()), name='acc_details'),
    path('change-password', login_required(ChangePassView.as_view()), name='change_pass'),
]
