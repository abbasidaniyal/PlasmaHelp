from django.urls import path

from users.views import  *

urlpatterns = [
    path('', home_page, name='home-page'),
    path('login/',LoginPageView.as_view(),name='login'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('register_donor/', DonorRegisterView.as_view(), name='register-donor'),
    path('register_hospital/', HospitalRegisterView.as_view(), name='register-hospital'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('hospital_dashboard',NearbyDonorView.as_view(),name="hospital-dashboard")
]
