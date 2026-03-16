from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import BulkAssignmentUploadForm, SubmissionForm
from .models import Assignment


@login_required
def assignment_list(request):
    assignments = Assignment.objects.all().order_by("-created_at")
    return render(
        request,
        "courses/assignment_list.html",
        {
            "assignments": assignments,
        },
    )


@login_required
def assignment_submission(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    success = False
    instance = None
    if request.method == "POST":
        # handle the form
        form = SubmissionForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            # let's add the id.
            # save file.
            instance = form.save(commit=False)
            # save the assingment information based on the id
            instance.assignment = assignment
            instance.save()
            success = True
    # create the form.
    else:
        form = SubmissionForm()
    return render(
        request,
        "courses/assignment_submission.html",
        {
            "assignment_id": assignment_id,
            "assignment": assignment,
            "form": form,
            "success": success,
            "submission": instance,
        },
    )


# Create your views here.
@login_required
def bulk_assignment_upload(request):
    success = False
    assignments = []
    if request.method == "POST":
        form = BulkAssignmentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded CSV file
            csv_file = form.cleaned_data["csv_file"]
            # Create assignments from the CSV file
            assignments = Assignment.create_assignments_from_csv(
                csv_file, owner=request.user
            )
            # Note
            success = True
    else:
        form = BulkAssignmentUploadForm()

    return render(
        request,
        "courses/bulk_assignment_upload.html",
        {
            "form": form,
            "success": success,
            "assignments": assignments,
        },
    )
