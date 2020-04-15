from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import FormView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import  reverse

from users.models import *
from users.forms import *

from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404


def home_page(request):
    return render(request,'index.html')

class LoginPageView(LoginView):
    template_name = 'login_page.html'
    redirect_field_name = 'home-page'
    redirect_authenticated_user = True

class LogoutPageView(LogoutView):
    next_page = 'home-page'
    template_name = 'logout_page.html'
    extra_context = {
        "logout" : "logout"
    }


class DonorRegisterView(CreateView):
    form_class = DonorUserForm
    template_name = 'register_donor.html'
    success_url = '/login/?next/signup_donor/'




class HospitalRegisterView(CreateView):

    form_class = HospitalUserForm
    template_name = 'register_hospital.html'
    success_url = '/login/?next=signup_hospital'


class ProfileView(LoginRequiredMixin, UpdateView):

    template_name = 'profile.html'
    success_url = '/'

    def get_object(self):
        user = self.request.user
        if self.request.user.user_type == "DONOR":
            self.model = DonorProfile
        else:
            self.model = HospitalProfile

        return get_object_or_404(self.model, user=user)

    def get_form_class(self):
        if self.request.user.user_type == "DONOR":
            return DonorProfileForm
        else:
            return HospitalProfileForm

    def form_valid(self, form):
        form.save(commit=False)
        obj = form.instance

        if self.request.user.user_type == "DONOR":
            if obj.mobile_number and obj.location and obj.birth_date and obj.report:
                obj.is_complete = True
            else:
                obj.is_complete = False

        else:
            if obj.mobile_number and obj.location and obj.hospital_name and obj.hospital_address and obj.mci_registeration_number:
                obj.is_complete = True
            else:
                obj.is_complete = False

        form.instance = obj
        form.save()
        return HttpResponseRedirect(self.success_url)