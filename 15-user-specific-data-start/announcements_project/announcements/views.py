from django.shortcuts import render, redirect
# import login_required decorator
from django.contrib.auth.decorators import (
    login_required, user_passes_test,
    permission_required)

# import the permission from core.
from core.permissions import is_teacher

# Create your views here.
from .models import Announcement
# import the announcement form
from .forms import AnnouncementForm

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(
        request,
        'announcements/announcement_list.html',
        {'announcements': announcements}
    )

# @user_passes_test(is_teacher)
@login_required
@permission_required('announcements.add_announcement', # permission
                     raise_exception=True) # raise a 403 page if they don't have permission.
def create_announcement(request):
    # request.user is on every request.
    # only teachers can create announcements
    # students cannot.
    if request.method == "POST":
        # create the form instance
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            # get an instance that's not saved
            # to the db yet.
            announcement = form.save(commit=False)
            # assign user to created_by field
            # on announcement instance and save.
            announcement.created_by = request.user
            announcement.save()

            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request,
        'announcements/create_announcement.html',
        {"form": form}
    )




