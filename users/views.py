from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import  reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView

from users.forms import *


def home_page(request):
    return render(request, 'index.html')


class LoginPageView(LoginView):
    template_name = 'login_page.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        return response


class LogoutPageView(LogoutView):
    next_page = 'home-page'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'Successfully logged out.')
        return response


class DonorRegisterView(CreateView):
    form_class = DonorUserForm
    template_name = 'register_donor.html'
    success_url = '/login/'


class HospitalRegisterView(CreateView):
    form_class = HospitalUserForm
    template_name = 'register_hospital.html'
    success_url = '/login/'


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
