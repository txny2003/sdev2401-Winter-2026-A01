from django.shortcuts import render, redirect

# Create your views here.
from .models import Announcement

# everyone can see if they're logged in.
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(
        request,
        'announcements/announcement_list.html',
        {'announcements': announcements}
    )

# restricted to teachers.
def create_announcement(request):
    return render(request, 'announcements/create_announcement.html')
