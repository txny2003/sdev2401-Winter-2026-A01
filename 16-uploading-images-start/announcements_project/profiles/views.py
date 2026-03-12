from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# import form and model
from .forms import ProfileForm
from .models import Profile


@login_required
def update_profile(request):
    # with the one to one mapping it will force the db
    # to have a single user to a single profile
    profile, created = Profile.objects.get_or_create(
        user=request.user,
    )

    if request.method == "POST":
        breakpoint()
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            return redirect("profile_edit")
    else:
        # get and other requests.
        form = ProfileForm(instance=profile)
    return render(
        request,
        "profiles/edit_profiles.html",
        {"form": form},
    )
