from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
# from django.contrib.auth.forms import UserChangeForm
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import DetailView, FormView, UpdateView

from .models import User
from .forms import BasicUserChangeForm


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "account/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "account/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "account/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "account/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "account/register.html")


class UserView(DetailView):
    """Render detailed user info."""

    model = User
    template_name = 'account/user_details.html'
    context_object_name = 'user_details'
    queryset = model.objects.all()

    def get_object(self, queryset=queryset):
        """Return an authenticated user."""

        return self.request.user

    def get_context_data(self, **kwargs):
        """Return context data."""

        context = super().get_context_data(**kwargs)
        return context

class ChangePassView(PasswordChangeView):
    """Change the account password."""

    template_name = "account/change_password.html"

class ChangePassDoneView(PasswordChangeDoneView):
    """Render a success page if a password has successfully changed."""

    template_name = "account/password_change_done.html"

class ChangeInfoView(UpdateView):
    """Change the account info."""

    model = User
    template_name = "account/change_info.html"
    form_class = BasicUserChangeForm
    success_url = 'details'

    def get_object(self, queryset=None):
        """Return the authenticated user."""

        return self.request.user
