from django.urls import path

from .views import bulk_assignment_upload, assignment_list, assignment_submission

urlpatterns = [
    path('bulk-assignment-upload/', bulk_assignment_upload, name='bulk_assignment_upload'),
    path('assignments/', assignment_list, name='assignment_list'),
    path('assignments/<int:assignment_id>/submit/', assignment_submission, name='assignment_submission'),
]
