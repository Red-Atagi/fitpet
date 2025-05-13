## Separate file for forms is standard for Django applications
from django import forms
## Django has built in UserCreation capabilities
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    name = forms.CharField(max_length=255, label="What’s your name?")
    pet_name = forms.CharField(max_length=255, label="Your Pet's Name?")

    class Meta:
        # Form is based on User Model
        model = User
        fields = ['username', 'password1', 'password2']


# Form to search for other users
class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
