from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, ListView, View
from django.forms.models import model_to_dict
from django.conf import settings
from profiles.forms import DonorProfileForm, HospitalProfileForm
from profiles.models import DonorProfile, HospitalProfile


class ProfileView(LoginRequiredMixin, View):
    template_name = "profiles/profile.html"

    def get(self, request, *args, **kwargs):

        if request.user.user_type == "DONOR":
            profile = DonorProfile.objects.get(user=request.user)
            form = DonorProfileForm
        elif self.request.user.user_type == "HOSPITAL":
            profile = HospitalProfile.objects.get(user=request.user)
            form = HospitalProfileForm
        else:
            raise PermissionDenied
        context = {
            "profile": profile,
            "profile_type": self.request.user.user_type,
            "api_key": settings.GOOGLE_MAP_API_KEY,
        }
        return render(request, self.template_name, context)


class ProfileEditView(LoginRequiredMixin, UpdateView):
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
            return DonorProfileForm
        elif self.request.user.user_type == "HOSPITAL":
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
