from django.db import models
from django.conf import settings


# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, # this is the model for the user
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title