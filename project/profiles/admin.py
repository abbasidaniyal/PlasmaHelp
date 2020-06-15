from django.contrib import admin

from profiles.models import DonorProfile, HospitalProfile


admin.site.register(DonorProfile)
admin.site.register(HospitalProfile)
