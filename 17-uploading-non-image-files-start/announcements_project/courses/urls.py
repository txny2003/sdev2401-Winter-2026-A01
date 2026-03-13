from django.urls import path
from .views import bulk_assignment_upload

urlpatterns = [
    path(
        "bulk-assignment-upload/",
        bulk_assignment_upload,
        name="bulk_assignment_upload",
    ),
]
