from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, ListView, View, CreateView
from django.contrib.gis.measure import D
from django.conf import settings
from django.core.mail import send_mail


from profiles.forms import (
    DonorProfileCreateForm,
    HospitalProfileCreateForm,
    DonorProfileEditForm,
    HospitalProfileEditForm,
    PatientProfileCreateForm,
    PatientProfileEditForm,
)
from profiles.models import DonorProfile, HospitalProfile, PatientProfile


class ProfileView(UserPassesTestMixin, LoginRequiredMixin, View):
    template_name = "profiles/profile.html"

    def get(self, request, *args, **kwargs):

        if request.user.user_type == "DONOR":
            profile = DonorProfile.objects.get(user=request.user)
        elif self.request.user.user_type == "HOSPITAL":
            profile = HospitalProfile.objects.get(user=request.user)
        elif self.request.user.user_type == "PATIENT":
            profile = PatientProfile.objects.get(user=request.user)
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
            elif self.request.user.user_type == "PATIENT":
                PatientProfile.objects.get(user=self.request.user)

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
        elif self.request.user.user_type == "PATIENT":
            self.model = PatientProfile
        else:
            self.model = None
        return get_object_or_404(self.model, user=user)

    def get_form_class(self):
        if self.request.user.user_type == "DONOR":
            return DonorProfileEditForm
        elif self.request.user.user_type == "HOSPITAL":
            return HospitalProfileEditForm
        elif self.request.user.user_type == "PATIENT":
            return PatientProfileEditForm

    def test_func(self):

        try:
            if self.request.user.user_type == "DONOR":
                DonorProfile.objects.get(user=self.request.user)
            elif self.request.user.user_type == "HOSPITAL":
                HospitalProfile.objects.get(user=self.request.user)
            elif self.request.user.user_type == "PATIENT":
                PatientProfile.objects.get(user=self.request.user)

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
        elif self.request.user.user_type == "PATIENT":
            return PatientProfileCreateForm

    def test_func(self):

        try:
            if self.request.user.user_type == "DONOR":
                DonorProfile.objects.get(user=self.request.user)
            elif self.request.user.user_type == "HOSPITAL":
                HospitalProfile.objects.get(user=self.request.user)
            elif self.request.user.user_type == "PATIENT":
                PatientProfile.objects.get(user=self.request.user)

            return False
        except:
            return True

    def handle_no_permission(self):
        return redirect("home-page")

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        
        if self.request.user.user_type == "HOSPITAL":
            send_mail(
                'A new hospital has registered on plasma help.',
                'A new hospital by the name of {} registered, located at {}. The person to be contacted is {} and reach him/her at {}'.format(object.hospital_name,object.hospital_address,object.contact_person_name,object.contact_person_mobile_number),
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
    fail_silently=False,
)

        return HttpResponseRedirect(self.success_url)


class NearbyDonorView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    template_name = "nearby_donor.html"
    model = DonorProfile
    paginate_by = 50

    def test_func(self):
        if self.request.user.user_type == "DONOR":
            raise PermissionDenied

        try:
            if hasattr(self.request.user, "hospitalprofile"):
                if not self.request.user.hospitalprofile.is_verified:
                    messages.warning(
                        self.request,
                        "Your profile has not been verified. Kindly wait for 2-3 days or contact us at plasma.help2020@gmail.com",
                    )

                    return False
                else:
                    return True
            elif hasattr(self.request.user, "patientprofile"):
                if not self.request.user.patientprofile.is_verified:
                    messages.warning(
                        self.request,
                        "Your profile has not been verified. Kindly wait for 6-8 hours or contact us at plasma.help2020@gmail.com incase of an emergency",
                    )
                    return False
                else:
                    return True
            else:

                raise Exception

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

        if self.request.user.user_type == "HOSPITAL":
            user_location = self.request.user.hospitalprofile.location
        elif self.request.user.user_type == "PATIENT":
            user_location = self.request.user.patientprofile.location

        query_set = DonorProfile.objects.filter(is_complete=True).filter(
            location__distance_lte=(user_location, D(km=distance))
        )
        for donor in query_set:
            donor.age = (date.today() - donor.birth_date).days // 365
            donor.distance = "{:.2f}".format(user_location.distance(donor.location))

        return sorted(query_set, key=lambda x: x.distance)

    def get_context_data(self, **kwargs):
        context = super(NearbyDonorView, self).get_context_data(**kwargs)
        try:
            context["filter"] = int(self.request.GET.get("filter", "20"))
        except ValueError:
            context["filter"] = 20

        return context
