from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from plasma_for_covid import settings
from profiles.validators import validate_file_extension, phone_regex
from users.models import User


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
    first_name = models.CharField("First Name", max_length=30, blank=False)
    last_name = models.CharField("Last Name", max_length=150, blank=False)
    is_complete = models.BooleanField(default=False)
    location = models.PointField(
        "Your Location (It will be kept confidential)", blank=False
    )
    birth_date = models.DateField("Date of Birth", blank=False)
    mobile_number = models.CharField(
        "Contact Number",
        validators=[phone_regex],
        max_length=15,
        blank=True,
        help_text="Format (+91xxxxxxxxxx)",
    )

    date_last_tested_negative = models.DateField(
        "Date Last Tested Negative for COVID19 ", blank=False
    )
    last_covid_report = models.FileField(
        "Last COVID19 Negative Test Report",
        null=True,
        blank=False,
        validators=[validate_file_extension],
        upload_to="last_donor_reports",
    )

    igg_report = models.FileField(
        "Immunoglobulin G (IgG) Test Report",
        blank=False,
        validators=[validate_file_extension],
        upload_to="igg_donor_reports",
    )

    def __str__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        if (
            self.location
            and self.last_covid_report
            and self.date_last_tested_negative
            and self.igg_report
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
    is_verified = models.BooleanField(default=False)

    hospital_name = models.CharField("Hospital Name", max_length=100, blank=False)
    hospital_address = models.CharField("Hospital Address", max_length=500, blank=False)
    location = models.PointField("Hospital Location ", blank=False)

    contact_person_name = models.CharField(
        "Contact Person Name", max_length=100, null=True, blank=False
    )
    contact_person_mobile_number = models.CharField(
        "Contact Number (+91xxxxxxxxxx)",
        validators=[phone_regex],
        max_length=15,
        blank=False,
    )

    mci_registration_number = models.CharField(
        "Medical Counsel of India Registration Number", max_length=50, blank=False
    )

    def __str__(self):
        return self.hospital_name

    def save(self, *args, **kwargs):
        if self.contact_person_name and self.contact_person_mobile_number:
            self.is_complete = True
        else:
            self.is_complete = False
        return super().save(*args, **kwargs)
