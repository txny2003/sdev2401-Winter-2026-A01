from django.urls import path

from .views import BulkAssignmentUploadView, AssignmentListView, AssignmentSubmissionView

urlpatterns = [
    path('bulk-assignment-upload/', BulkAssignmentUploadView.as_view(), name='bulk_assignment_upload'),
    path('assignments/', AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/<int:assignment_id>/submit/', AssignmentSubmissionView.as_view(), name='assignment_submission'),
]
