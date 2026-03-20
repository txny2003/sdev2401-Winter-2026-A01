from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import BulkAssignmentUploadForm
from .models import Assignment

# rewrite using Class based views
# update the urls.


@method_decorator(login_required, name="dispatch")
class AssignmentListView(View):
    template_name = "courses/assignment_list.html"

    def get(self, request):
        assignments = Assignment.objects.all().order_by("-created_at")

        return render(
            request,
            self.template_name,
            {
                "assignments": assignments,
            },
        )


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


@method_decorator(login_required, name="dispatch")
class AssignmentSubmissionView(View):
    template_name = "courses/assignment_submission.html"

    def get(self, request, assignment_id):
        # note: we created the form part in class
        # look at previous notes to fix this
        # submission view woo.
        return render(
            request,
            self.template_name,
            {
                "assignment_id": assignment_id,
            },
        )


@login_required
def assignment_submission(request, assignment_id):
    # Placeholder for submission view
    return render(
        request,
        "courses/assignment_submission.html",
        {
            "assignment_id": assignment_id,
        },
    )


class BulkAssignmentUploadView(View):
    template_name = "courses/bulk_assignment_upload.html"
    form_class = BulkAssignmentUploadForm

    def get(self, request):
        form = self.form_class()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "success": False,
                "assignments": [],
            },
        )

    def post(self, request):
        form = self.form_class(
            request.POST,
            request.FILES,
        )
        success = False
        if form.is_valid():
            # Process the uploaded CSV file
            csv_file = form.cleaned_data["csv_file"]
            # Create assignments from the CSV file
            assignments = Assignment.create_assignments_from_csv(
                csv_file, owner=request.user
            )
            # Note
            success = True
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "success": success,
                "assignments": assignments,
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
