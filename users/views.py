from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordChangeView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, FormView, View

from users.forms import *
from users.mixins import LoginNotRequiredMixin
from users.utils import send_mail_to_user, TokenGenerator

from profiles.models import HospitalProfile, DonorProfile


def activate(request, uidb64, token):
    logout(request)

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

    return redirect("/")


class ResendVerification(LoginNotRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ResendActivationEmailForm
    template_name = "resend_activation.html"
    redirect_field_name = "home-page"

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

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if (
                self.request.user.user_type == "DONOR"
                and len(DonorProfile.objects.filter(user=self.request.user)) is 0
            ):
                return "/profile/create"
            elif (
                self.request.user.user_type == "HOSPITAL"
                and len(HospitalProfile.objects.filter(user=self.request.user)) is 0
            ):
                return "/profile/create"
        return "/"

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


class DonorRegisterView(LoginNotRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = DonorUserForm
    template_name = "register_donor.html"
    success_url = "/"
    success_message = "Thank you for registration. We have sent you an email. Kindly verify your Account."
    redirect_field_name = "home-page"

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail_to_user(self.request, self.object)
        return response


class HospitalRegisterView(LoginNotRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = HospitalUserForm
    template_name = "register_hospital.html"
    success_url = "/"
    success_message = "Thank you for registration. We have sent you an email. Kindly verify your Account."
    redirect_field_name = "home-page"

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail_to_user(self.request, self.object)
        return response


class DeleteUserView(LoginRequiredMixin, View):
    model = User
    success_url = "/"
    template_name = "user_delete_confirm.html"
    redirect_field_name = "login"

    def get(self, request):
        return render(request, template_name=self.template_name)

    def post(self, request):
        if "delete" in request.POST:
            self.request.user.delete()
        return HttpResponseRedirect(self.success_url)
