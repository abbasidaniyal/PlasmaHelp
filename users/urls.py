from django.urls import path
from django.views.generic import TemplateView

from users.views import  *

urlpatterns = [
    path('register_donor/', DonorUserSignupView.as_view(), name='register-donor'),
    path('register_hospital/', HospitalUserSignupView.as_view(), name='register-hospital'),
    path('signup_hospital/', HospitalProfileSignupView.as_view(), name='hospital-profile-signup'),
    path('signup_donor/', DonorProfileSignupView.as_view(), name='donor-profile-signup'),
]
