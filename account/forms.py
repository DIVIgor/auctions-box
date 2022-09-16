from django.contrib.auth.forms import UserChangeForm, UsernameField
# from django.forms import ModelForm

from .models import User


class BasicUserChangeForm(UserChangeForm):
    """A form to change user's info.
    A `username` field fills by the template.
    Fields: `first_name`, `last_name`, `email`.
    """

    password = None

    class Meta:
        model = User
        readonly_fields = ('username',)
        fields = ('first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}
