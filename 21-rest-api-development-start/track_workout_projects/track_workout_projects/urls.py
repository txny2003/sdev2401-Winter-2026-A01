from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # comment out this line
    path("api/v1/", include("workouts_app.urls")),
]
