from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

# import our new form here
from .forms import UserRegistrationForm

# let's create the view to register a user
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() # save the new user to the database
            login(request, user)

            # redirect the user on successful form submission to
            # the annoucements list
            return redirect("announcement_list")
            # where "announcement_list" is the name of the url
            # to redirect to.

    form = UserRegistrationForm()
    return render(
        request,
        'core/register.html',
        { "form": form }
    )