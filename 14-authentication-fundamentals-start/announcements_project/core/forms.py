from django import forms
# use the built in user creation form but we're going to
# edit it to use our new role field.
from django.contrib.auth.forms import UserCreationForm
# UserCreationForm inherits from model form.
# use the same idea as a model form but with our User model
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            # from the AbstractUser model
            'username',
            'email',
            'password1',
            'password2',
            # our new role
            'role'
        ]
