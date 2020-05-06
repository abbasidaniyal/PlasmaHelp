from django.contrib import admin

from profiles.models import DonorProfile, HospitalProfile

# Register your models here.
admin.site.register(DonorProfile)
admin.site.register(HospitalProfile)
