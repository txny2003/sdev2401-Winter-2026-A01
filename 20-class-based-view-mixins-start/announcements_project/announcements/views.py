from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

# import login_required decorator
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)

# Create your views here.
from .models import Announcement
from .forms import AnnouncementForm

# let's import our mixin
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import IsTeacherRoleMixin


# our test function here.
def is_teacher(user):
    # the user object is passed in here by the decorator
    return user.role == "teacher"


class AnnouncementListView(LoginRequiredMixin, View):
    template_name = "announcements/announcement_list.html"

    def get(self, request):
        announcements = Announcement.objects.all().order_by("-created_at")
        return render(request, self.template_name, {"announcements": announcements})


# below we're using multiple mixins
# to achieve the same functionality as before.
class CreateAnnouncementView(
    LoginRequiredMixin,
    IsTeacherRoleMixin,
    View,
):
    template_name = "announcements/create_announcement.html"
    form_class = AnnouncementForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            return redirect("announcement_list")
        return render(request, self.template_name, {"form": form})
