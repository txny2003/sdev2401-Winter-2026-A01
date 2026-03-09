from django.urls import path
from .views import AnnouncementListView, CreateAnnouncementView

urlpatterns = [
    path('', AnnouncementListView.as_view(), name='announcement_list'),
    path('create/', CreateAnnouncementView.as_view(), name='create_announcement'),
]
