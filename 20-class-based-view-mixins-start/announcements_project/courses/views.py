from django.views import View
from django.utils.decorators import method_decorator

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import BulkAssignmentUploadForm
from .models import Assignment


@method_decorator(login_required, name='dispatch')
class AssignmentListView(View):
    template_name = 'courses/assignment_list.html'

    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.all().order_by('-created_at')
        return render(request, self.template_name, {
            'assignments': assignments,
        })


@method_decorator(login_required, name='dispatch')
class AssignmentSubmissionView(View):
    template_name = 'courses/assignment_submission.html'

    def get(self, request, assignment_id, *args, **kwargs):
        return render(request, self.template_name, {
            'assignment_id': assignment_id,
        })

class BulkAssignmentUploadView(View):
    template_name = 'courses/bulk_assignment_upload.html'
    form_class = BulkAssignmentUploadForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        success = False
        assignments = []
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            assignments = Assignment.create_assignments_from_csv(csv_file, owner=request.user)
            success = True
        return render(request, self.template_name, {
            'form': form,
            'success': success,
            'assignments': assignments,
        })