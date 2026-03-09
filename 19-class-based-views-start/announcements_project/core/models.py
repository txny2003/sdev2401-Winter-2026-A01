from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # this is just a way to restrict a character field to two
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # this is purely for convenience when we print out a user object
    def __str__(self):
        return f"{self.username} ({self.role})"