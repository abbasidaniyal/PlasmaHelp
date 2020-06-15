from django.urls import path, include

from profiles.views import ProfileView, ProfileEditView, ProfileCreateView

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("edit/", ProfileEditView.as_view(), name="profile-edit"),
    path("create/", ProfileCreateView.as_view(), name="profile-create"),
]
