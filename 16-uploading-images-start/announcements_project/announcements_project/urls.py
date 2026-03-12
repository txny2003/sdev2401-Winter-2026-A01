from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("core.urls")),  # registration view added!
    path("announcements/", include("announcements.urls")),  # announcements app urls
    path("profiles/", include("profiles.urls")),
]

# we need our project to serve the urls of media
# again this is going to be different in production.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
