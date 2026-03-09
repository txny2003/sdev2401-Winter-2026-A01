from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm

from profiles.models import Profile

@login_required
def profile_list(request):

    profiles = Profile.objects.all()
    # as an optimization we can use select_related to fetch the related user objects in a single query this is an advance topic covered in future courses.
    # profiles = Profile.objects.select_related('user').all()
    return render(request, 'profiles/profile_list.html', {'profiles': profiles})

@login_required
def edit_profile(request):
    # create the profile if it doesn't exist or get it if it does.
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')  # Redirect to the same profile page after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form, 'profile': profile})