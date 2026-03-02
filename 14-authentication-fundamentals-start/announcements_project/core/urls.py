from django.urls import path

from .views import register

urlpattern = [
    path('register/', register, name="register")
]