from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as geo_models
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from plasma_for_covid import settings
from users.managers import CustomUserManager
from users.validators import validate_file_extension, phone_regex


class User(AbstractUser):
    user_options = [("DONOR", "Donor"), ("HOSPITAL", "Hospital")]
    user_type = models.CharField(
        max_length=20, choices=user_options, null=False, blank=False
    )
    email = models.EmailField("email address", unique=True, null=True)
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class DonorProfile(models.Model):
    """
    Donor profile details.

    :parameter
    user : One to one mapping with the django user model
    birth_day : Date of Birth of user
    email : Email Address of the Donor
    mobile_number : Mobile Number of Donor (optional)
    report : COVID Report of Donor

    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    first_name = models.CharField("First Name", max_length=30, blank=True)
    last_name = models.CharField("Last Name", max_length=150, blank=True)
    is_complete = models.BooleanField(default=False)
    location = geo_models.PointField(
        "Your Location (It will be kept confidential)", null=True, blank=True
    )
    birth_date = models.DateField("Date of Birth", null=True, blank=True)

    mobile_number = models.CharField(
        "Contact Number (+91xxxxxxxxxx)",
        validators=[phone_regex],
        max_length=15,
        blank=True,
    )
    last_covid_report = models.FileField(
        "Last COVID19 Negative Test Report",
        null=True,
        blank=True,
        validators=[validate_file_extension],
        upload_to="last_donor_reports",
    )

    date_last_tested_negative = models.DateField(
        "Date Last Tested Negative for COVID19 ", null=True, blank=True
    )

    igg_report = models.FileField(
        "Immunoglobulin G (IgG) Test Report",
        null=True,
        blank=True,
        validators=[validate_file_extension],
        upload_to="igg_donor_reports",
    )

    def __str__(self):
        if (self.first_name and self.last_name) is not None:
            return self.first_name + " " + self.last_name
        return "NOT CREATED"

    def save(self, *args, **kwargs):
        if (
            self.mobile_number
            and self.location
            and self.birth_date
            and self.last_covid_report
            and self.first_name
            and self.last_name
            and self.date_last_tested_negative
        ):
            self.is_complete = True
        else:
            self.is_complete = False
        return super().save(*args, **kwargs)


class HospitalProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    is_complete = models.BooleanField(default=False)
    hospital_name = models.CharField(
        "Hospital Name", max_length=100, null=True, blank=True
    )
    hospital_address = models.TextField(
        "Hospital Address", max_length=500, null=True, blank=True
    )
    location = geo_models.PointField("Hospital Location ", null=True, blank=True)

    contact_person_name = models.CharField(
        "Contact Person Name", max_length=100, null=True, blank=True
    )
    contact_person_mobile_number = models.CharField(
        "Contact Number (+91xxxxxxxxxx)",
        validators=[phone_regex],
        max_length=15,
        blank=True,
    )

    mci_registration_number = models.CharField(
        "Medical Counsel of India Registration Number",
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.hospital_name:
            return self.hospital_name
        else:
            return "NOT CREATED"

    def save(self, *args, **kwargs):
        if (
            self.contact_person_name
            and self.contact_person_mobile_number
            and self.location
            and self.hospital_name
            and self.hospital_address
            and self.mci_registration_number
            and self.contact_person_name
            and self.contact_person_mobile_number
        ):
            self.is_complete = True
        else:
            self.is_complete = False
        return super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "DONOR":
            profile = DonorProfile.objects.create(user=instance)
        else:
            profile = HospitalProfile.objects.create(user=instance)

        profile.save()
