from django.shortcuts import render, redirect
# import login_required decorator
from django.contrib.auth.decorators import login_required

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
def create_announcement(request):
    # only teachers can create announcements
    # students cannot.
    return render(request, 'announcements/create_announcement.html', {})