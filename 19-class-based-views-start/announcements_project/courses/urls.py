from django.urls import path

from .views import (
    bulk_assignment_upload,
    assignment_list,
    assignment_submission,
    AssignmentListView,
    AssignmentSubmissionView,
)

urlpatterns = [
    path(
        "bulk-assignment-upload/", bulk_assignment_upload, name="bulk_assignment_upload"
    ),
    # CBV
    path(
        "assignments/",
        AssignmentListView.as_view(),
        name="assignment_list",
    ),
    # FBV
    # path("assignments/", assignment_list, name="assignment_list"),
    # CBV
    path(
        "assignments/<int:assignment_id>/submit/",
        AssignmentSubmissionView.as_view(),
        name="assignment_submission",
    ),
    # FBV
    # path(
    #     "assignments/<int:assignment_id>/submit/",
    #     assignment_submission,
    #     name="assignment_submission",
    # ),
]
