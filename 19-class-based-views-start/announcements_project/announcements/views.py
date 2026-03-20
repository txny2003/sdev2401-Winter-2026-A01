from django.views import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

# import login_required decorator
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required,
)

# Create your views here.
from .models import Announcement
from .forms import AnnouncementForm


# our test function here.
def is_teacher(user):
    # the user object is passed in here by the decorator
    return user.role == "teacher"


# this is how to use function decorators on class based
# views "dispatch" is the function that the view will
# protect (which goes to get, post, etc.)
@method_decorator(login_required, name="dispatch")
class AnnouncementListView(View):
    template_name = "announcements/announcement_list.html"

    def get(self, request):
        announcements = Announcement.objects.all().order_by("-created_at")
        return render(
            request,
            self.template_name,
            {"announcements": announcements},
        )


# write this as a class based view and fix
# the url based on it.
@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by("-created_at")
    return render(
        request,
        "announcements/announcement_list.html",
        {"announcements": announcements},
    )


# rewrite this below as a class based views
# add the url
# refer to the slides if you're confused.


class CreateAnnouncementView(View):
    template_name = "announcements/create_announcement.html"
    form_class = AnnouncementForm

    # handling the request.method of get
    def get(self, request):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {"form": form},
        )

    # handling the request.method of post
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            # the commit false will prevent the form from saving to the database
            # set the created_by field to the current user
            announcement.created_by = request.user
            announcement.save()
            # save the announcement to the database.
            return redirect("announcement_list")
        return render(
            request,
            self.template_name,
            {"form": form},
        )


# this will restrict access to only users that pass the is_teacher test
# it will redirect to the login page if the user does not have permission.
@login_required
@user_passes_test(is_teacher, login_url="login")
# @permission_required('announcements.add_announcement', raise_exception=True) # the optional section
def create_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            # the commit false will prevent the form from saving to the database
            # set the created_by field to the current user
            announcement.created_by = request.user
            announcement.save()
            # save the announcement to the database.
            return redirect("announcement_list")
    else:
        form = AnnouncementForm()
    return render(request, "announcements/create_announcement.html", {"form": form})
