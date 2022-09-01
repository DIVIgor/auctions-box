from django.contrib.auth.forms import UserChangeForm, UsernameField
# from django.forms import ModelForm

from .models import User


class BasicUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        readonly_fields = ('username',)
        fields = ('first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}
