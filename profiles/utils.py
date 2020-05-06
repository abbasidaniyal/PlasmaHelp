from profiles.models import DonorProfile, HospitalProfile


def get_profile(user):
    try:
        if user.user_type == "DONOR":
            return DonorProfile.objects.get(user=user)
        elif user.user_type == "HOSPITAL":
            return HospitalProfile.objects.get(user=user)
    except:
        return False
