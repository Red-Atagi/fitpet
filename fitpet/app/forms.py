## Separate file for forms is standard for Django applications
from django import forms
## Django has built in UserCreation capabilities
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        # Form is based on User Model
        model = User
        fields = ['username', 'password1', 'password2']
