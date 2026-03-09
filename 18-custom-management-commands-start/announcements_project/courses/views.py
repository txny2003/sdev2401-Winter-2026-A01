from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import BulkAssignmentUploadForm
from .models import Assignment


@login_required
def assignment_list(request):
    assignments = Assignment.objects.all().order_by('-created_at')
    return render(request, 'courses/assignment_list.html', {
        'assignments': assignments,
    })

@login_required
def assignment_submission(request, assignment_id):
    # Placeholder for submission view
    return render(request, 'courses/assignment_submission.html', {
        'assignment_id': assignment_id,
    })

# Create your views here.
@login_required
def bulk_assignment_upload(request):
    success = False
    assignments = []
    if request.method == 'POST':
        form = BulkAssignmentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded CSV file
            csv_file = form.cleaned_data['csv_file']
            # Create assignments from the CSV file
            assignments = Assignment.create_assignments_from_csv(csv_file, owner=request.user)
            # Note
            success = True
    else:
        form = BulkAssignmentUploadForm()

    return render(request, 'courses/bulk_assignment_upload.html', {
        'form': form,
        'success': success,
        'assignments': assignments,
    })