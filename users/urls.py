from django.contrib.auth import views as views
from django.urls import path

from users.views import (
    LoginPageView,
    LogoutPageView,
    CustomPasswordResetView,
    CustomPasswordChangeView,
    DonorRegisterView,
    HospitalRegisterView,
    ProfileView,
    DeleteUserView,
    ResendVerification,
    NearbyDonorView,
    activate,
)

urlpatterns = [
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", LogoutPageView.as_view(), name="logout"),
    path("register_donor/", DonorRegisterView.as_view(), name="register-donor"),
    path(
        "register_hospital/", HospitalRegisterView.as_view(), name="register-hospital"
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/delete", DeleteUserView.as_view(), name="delete-user"),
    path("hospital_dashboard", NearbyDonorView.as_view(), name="hospital-dashboard"),
    path("activate/<str:uidb64>/<str:token>/", activate, name="activate"),
    path(
        "resend_verification_link/",
        ResendVerification.as_view(),
        name="resend-verification",
    ),
    path(
        "password_change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
