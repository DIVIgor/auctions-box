from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView, CreateView, UpdateView

from .forms import RegisterFrom, BasicUserChangeForm


User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterFrom
    template_name = 'account/register.html'

class LogInView(LoginView):
    template_name = 'account/login.html'

class LogOutView(LogoutView):
    pass

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
