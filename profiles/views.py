from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, ListView, View, CreateView
from django.contrib.gis.measure import D
from django.conf import settings

from profiles.forms import (
    DonorProfileCreateForm,
    HospitalProfileCreateForm,
    DonorProfileEditForm,
    HospitalProfileEditForm,
)
from profiles.models import DonorProfile, HospitalProfile


class ProfileView(UserPassesTestMixin, LoginRequiredMixin, View):
    template_name = "profiles/profile.html"

    def get(self, request, *args, **kwargs):

        if request.user.user_type == "DONOR":
            profile = DonorProfile.objects.get(user=request.user)
        elif self.request.user.user_type == "HOSPITAL":
            profile = HospitalProfile.objects.get(user=request.user)
        else:
            raise PermissionDenied
        context = {
            "profile": profile,
            "profile_type": self.request.user.user_type,
            "api_key": settings.GOOGLE_MAP_API_KEY,
        }
        return render(request, self.template_name, context)

    def test_func(self):

        try:
            if self.request.user.user_type == "DONOR":
                DonorProfile.objects.get(user=self.request.user)
            elif self.request.user.user_type == "HOSPITAL":
                HospitalProfile.objects.get(user=self.request.user)

            return True
        except:
            return False

    def handle_no_permission(self):
        messages.warning(self.request, "Kindly create your profile first.")
        return redirect("profile-create")


class ProfileEditView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = "profiles/profile_edit.html"
    success_url = "/"

    def get_object(self, **kwargs):
        user = self.request.user
        if self.request.user.user_type == "DONOR":
            self.model = DonorProfile
        elif self.request.user.user_type == "HOSPITAL":
            self.model = HospitalProfile
        else:
            self.model = None
        return get_object_or_404(self.model, user=user)

    def get_form_class(self):
        if self.request.user.user_type == "DONOR":
            return DonorProfileEditForm
        elif self.request.user.user_type == "HOSPITAL":
            return HospitalProfileEditForm

    def test_func(self):

        try:
            if self.request.user.user_type == "DONOR":
                DonorProfile.objects.get(user=self.request.user)
            elif self.request.user.user_type == "HOSPITAL":
                HospitalProfile.objects.get(user=self.request.user)

            return True
        except:
            return False

    def handle_no_permission(self):
        messages.warning(self.request, "Kindly create your profile first.")
        return redirect("profile-create")


class ProfileCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = "profiles/profile_create.html"
    success_url = "/profile/"

    def get_form_class(self):
        if self.request.user.user_type == "DONOR":
            return DonorProfileCreateForm
        elif self.request.user.user_type == "HOSPITAL":
            return HospitalProfileCreateForm

    def test_func(self):

        try:
            if self.request.user.user_type == "DONOR":
                DonorProfile.objects.get(user=self.request.user)
            elif self.request.user.user_type == "HOSPITAL":
                HospitalProfile.objects.get(user=self.request.user)

            return False
        except:
            return True

    def handle_no_permission(self):
        return redirect("home-page")

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return HttpResponseRedirect(self.success_url)


class NearbyDonorView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    template_name = "nearby_donor.html"
    model = DonorProfile
    paginate_by = 50

    def test_func(self):
        if self.request.user.user_type == "DONOR":
            raise PermissionDenied

        try:
            if isinstance(self.request.user.hospitalprofile, HospitalProfile):
                if not self.request.user.hospitalprofile.is_verified:
                    messages.warning(
                        self.request,
                        "Your profile has not been verified. Kindly wait for 2-3 days or contact us at plasma.help2020@gmail.com",
                    )
                    return False
                else:
                    return True
        except:
            messages.warning(self.request, "Kindly create your profile first.")
            return False

    def handle_no_permission(self):
        return redirect("profile-create")

    def get_queryset(self):
        try:
            distance = int(self.request.GET.get("filter", "20"))
        except ValueError:
            distance = 20

        from datetime import date

        hospital_location = self.request.user.hospitalprofile.location
        query_set = DonorProfile.objects.filter(is_complete=True).filter(
            location__distance_lte=(hospital_location, D(km=distance))
        )
        for donor in query_set:
            donor.age = (date.today() - donor.birth_date).days // 365
            donor.distance = "{:.2f}".format(hospital_location.distance(donor.location))

        return sorted(query_set, key=lambda x: x.distance)

    def get_context_data(self, **kwargs):
        context = super(NearbyDonorView, self).get_context_data(**kwargs)
        try:
            context["filter"] = int(self.request.GET.get("filter", "20"))
        except ValueError:
            context["filter"] = 20

        return context
