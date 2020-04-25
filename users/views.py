# from django.urls import  reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import *
from users.utils import send_mail, TokenGenerator


def home_page(request):
    return render(request, "index.html")


def about_page(request):
    return render(request, "about.html")


def activate(request, uidb64, token):
    # try:
    print(uidb64, token)
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    #     user = None
    print(user)
    if user is not None and TokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
    else:
        messages.error(request, "Activation link is invalid!")

    return render(request, "index.html")


class LoginPageView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class LogoutPageView(LogoutView):
    next_page = "home-page"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, "Successfully logged out.")
        return response


class DonorRegisterView(SuccessMessageMixin, CreateView):
    form_class = DonorUserForm
    template_name = "register_donor.html"
    success_url = "/"
    success_message = "Thank you for registration. We have sent you an email. Kindly verify your Account."

    def form_valid(self, form):
        response = super().form_valid(form)

        send_mail(self.request, self.object)
        return response


class HospitalRegisterView(SuccessMessageMixin, CreateView):
    form_class = HospitalUserForm
    template_name = "register_hospital.html"
    success_url = "/"
    success_message = "Thank you for registration. We have sent you an email. Kindly verify your Account."

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail(self.request, self.object)

        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "profile.html"
    success_url = "/"

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
            if (
                obj.mobile_number
                and obj.location
                and obj.hospital_name
                and obj.hospital_address
                and obj.mci_registeration_number
            ):
                obj.is_complete = True
            else:
                obj.is_complete = False

        form.instance = obj
        form.save()
        return HttpResponseRedirect(self.success_url)


class NearbyDonorView(LoginRequiredMixin, ListView):
    template_name = "nearby_donor.html"
    model = DonorProfile
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):

        if request.user.user_type == "DONOR":
            raise PermissionDenied

        elif request.user.hospitalprofile.is_complete is False:
            messages.warning(
                request, "Complete your profile in order to view the Dashboard"
            )
            return redirect("profile",)
        else:
            response = super().dispatch(request, *args, **kwargs)
        return response

    def get_queryset(self):
        try:
            distance = int(self.request.GET.get("filter", "50"))
        except ValueError:
            distance = 50

        lst = []
        for donor in DonorProfile.objects.all().filter(is_complete=True):
            if (
                self.request.user.hospitalprofile.location.distance(donor.location)
                * 100
                <= distance
            ):
                lst.append(donor)
        return lst

    def get_context_data(self, **kwargs):
        context = super(NearbyDonorView, self).get_context_data(**kwargs)

        try:
            context["filter"] = int(self.request.GET.get("filter", "50"))
        except ValueError:
            context["filter"] = 50

        return context
