from django.shortcuts import render, redirect
# import login_required decorator
from django.contrib.auth.decorators import (
    login_required, user_passes_test)

# import the permission from core.
from core.permissions import is_teacher

# Create your views here.
from .models import Announcement


@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(
        request,
        'announcements/announcement_list.html',
        {'announcements': announcements}
    )


@login_required
@user_passes_test(is_teacher)
def create_announcement(request):
    # request.user is on every request.
    # only teachers can create announcements
    # students cannot.
    return render(request, 'announcements/create_announcement.html', {})