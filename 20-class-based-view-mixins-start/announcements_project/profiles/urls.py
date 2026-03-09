from django.urls import path

from .views import edit_profile, profile_list

urlpatterns = [
    path('edit/', edit_profile, name='profile_edit'),
    path('', profile_list, name='profile_list'),
]