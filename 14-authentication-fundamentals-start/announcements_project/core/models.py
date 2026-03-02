from django.db import models
# we're going to import AbstractUser
# the class that will override the user model.
from django.contrib.auth.models import AbstractUser

# the user we'll use in our application here.
class User(AbstractUser):
    # a tuple of tuples (lists that do not change.)
    ROLE_CHOICES = (
        ('teacher', "Teacher")
        ('teacher', "Student")
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        # username is from the abstractuser
        return f"{self.username} ({self.role})"