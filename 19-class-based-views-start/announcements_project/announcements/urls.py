from django.urls import path
from .views import (
    AnnouncementListView,
    CreateAnnouncementView,
    announcement_list,
    create_announcement,
)

urlpatterns = [
    # the class based url view.
    path(
        "",
        AnnouncementListView.as_view(),
        name="announcement_list",
    ),
    # below is the function base view.
    # path(
    #     "",
    #     announcement_list,
    #     name="announcement_list",
    # ),
    path(
        "create/",
        CreateAnnouncementView.as_view(),
        name="create_announcement",
    ),
    # path("create/", create_announcement, name="create_announcement"),
]
