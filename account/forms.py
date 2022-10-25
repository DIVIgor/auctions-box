from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.forms import EmailField

from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterFrom(UserCreationForm):
    """A form to create a new user account."""

    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

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
