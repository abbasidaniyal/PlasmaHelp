from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordChangeView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, ListView, FormView

from users.forms import *
from users.utils import send_mail_to_user, TokenGenerator


def activate(request, uidb64, token):

    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

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


class ResendVerification(SuccessMessageMixin, FormView):
    form_class = ResendActivationEmailForm
    template_name = "resend_activation.html"

    success_url = "/"
    success_message = "We have sent you an email with the verification link."

    def form_valid(self, form):
        response = super().form_valid(form)

        user = User.objects.get(email=form.cleaned_data.get("email"))
        send_mail_to_user(self.request, user)
        return response


class LoginPageView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    authentication_form = LoginForm

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        if "This account is inactive." in form.errors["__all__"][0]:
            form.errors["__all__"][0] = format_html(
                """You account is not active. Kindly check you mail. 
                If you have not received any mail, <a href='{}'>Click Here</a>""",
                reverse("resend-verification"),
            )

        return self.render_to_response(self.get_context_data(form=form))


class LogoutPageView(LogoutView):
    next_page = "home-page"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, "Successfully logged out.")
        return response


class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm


class DonorRegisterView(SuccessMessageMixin, CreateView):
    form_class = DonorUserForm
    template_name = "register_donor.html"
    success_url = "/"
    success_message = "Thank you for registration. We have sent you an email. Kindly verify your Account."

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail_to_user(self.request, self.object)
        return response


class HospitalRegisterView(SuccessMessageMixin, CreateView):
    form_class = HospitalUserForm
    template_name = "register_hospital.html"
    success_url = "/"
    success_message = "Thank you for registration. We have sent you an email. Kindly verify your Account."

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail_to_user(self.request, self.object)
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
        from datetime import date

        for donor in DonorProfile.objects.all().filter(is_complete=True):
            tmp = (
                self.request.user.hospitalprofile.location.distance(donor.location)
                * 100
            )
            if tmp <= distance:
                donor.distance = "{:.1f}".format(tmp)
                donor.age = (date.today() - donor.birth_date).days // 365
                lst.append(donor)

        return lst

    def get_context_data(self, **kwargs):
        context = super(NearbyDonorView, self).get_context_data(**kwargs)

        try:
            context["filter"] = int(self.request.GET.get("filter", "50"))
        except ValueError:
            context["filter"] = 50

        return context
