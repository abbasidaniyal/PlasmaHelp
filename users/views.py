from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.views.generic import FormView

from users.forms import *


class DonorUserSignupView(FormView):
    form_class = DonorUserForm
    template_name = 'register_donor.html'
    success_url = '/users/signup_donor/'


class DonorProfileSignupView(FormView):
    form_class = DonorProfileForm
    template_name = 'donor_signup.html'
    success_url = '/login/'


class HospitalUserSignupView(FormView):
    form_class = HospitalUserForm
    template_name = 'register_hospital.html'
    success_url = '/users/signup_hospital/'


class HospitalProfileSignupView(FormView):
    form_class = HospitalProfileForm
    template_name = 'register_hospital.html'
    success_url = '/login/'
