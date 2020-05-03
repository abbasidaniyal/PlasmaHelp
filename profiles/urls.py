from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from plasma_for_covid import settings
from profiles.views import *

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("edit/", ProfileEditView.as_view(), name="profile-edit"),
]
