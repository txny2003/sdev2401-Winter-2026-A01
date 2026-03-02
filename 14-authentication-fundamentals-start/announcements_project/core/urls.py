from django.urls import path
# let's import the default LoginView
from django.contrib.auth.views import LoginView, LogoutView

from .views import register


urlpatterns = [
    path('register/', register, name="register"),
    # the login view is class based
    # more on this later
    path("login/", LoginView.as_view(
        template_name="core/login.html"
    ), name="login"),
    # we're also going to add the logout view which is a form.
    path("logout", LogoutView.as_view(), name="logout")
]