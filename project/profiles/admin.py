from django.contrib import admin

from profiles.models import DonorProfile, HospitalProfile, PatientProfile

admin.site.register(DonorProfile)
admin.site.register(HospitalProfile)
admin.site.register(PatientProfile)
