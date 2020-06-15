from functools import wraps

from django.contrib import messages

from profiles.models import HospitalProfile, DonorProfile


def profile_incomplete_check(view):
    @wraps(view)
    def meathod(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                if request.user.user_type == "DONOR":
                    DonorProfile.objects.get(user=request.user)
                elif request.user.user_type == "HOSPITAL":
                    HospitalProfile.objects.get(user=request.user)
            except:
                messages.warning(
                    request,
                    "Your profile is not complete. Go to the profile section to complete it.",
                )
        return view(request, *args, **kwargs)

    return meathod
