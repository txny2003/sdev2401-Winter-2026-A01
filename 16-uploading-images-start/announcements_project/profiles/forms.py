from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "profile_picture",
        ]

        # profile picture is going to
        # be an image field that will
        # render a file input in the
        # template.
