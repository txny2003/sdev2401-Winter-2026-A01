from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            # inherited field from the creation forms
            'username',
            'email',
            'password1',
            'password2',
            # our custom field!
            'role'
        ]
