from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required

# from .views import register
from .views import (RegisterView, LogInView, LogOutView, UserView,
    ChangeInfoView, ChangePassView, ChangePassDoneView)


app_name = 'account'

urlpatterns = [
    path('login', LogInView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(success_url=reverse_lazy(
        'account:login')), name='register'),
    path('details', login_required(UserView.as_view()), name='acc_details'),
    path('change-password', login_required(
        ChangePassView.as_view(success_url=reverse_lazy(
            'account:password_change_done'))),
        name='change_pass'),

    path('change-password/success', login_required(
        ChangePassDoneView.as_view()),
        name='password_change_done'),

    path('change-info', login_required(ChangeInfoView.as_view()),
        name='change_info'),
]
