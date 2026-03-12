from django.db import models

# import settings because we want to point to the correct user.
from django.conf import settings


class Profile(models.Model):
    # this is a relationship a lot like a foreign key except it restricts
    # one user to one profile.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # if i delete the user, I delete the prifle.
        related_name="profile",
    )
    bio = models.TextField(blank=True, null=True)
    # we're going add the image file.
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",  # will upload to `media/profile_pictures/`
        blank=True,
        null=True,
    )
    # this is going to store items in settings.MEDIA_ROOT
    # and serve them from the url settings.MEDIA_URL
    # note it's good to keep things organized in your media.

    def __str__(self):
        # we can access the user fields based on the user relationship.
        return f"profile of {self.user.username}"
