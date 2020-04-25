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
    report = models.FileField(
        "COVID19 Report",
        null=True,
        blank=True,
        validators=[validate_file_extension],
        upload_to="donor_reports",
    )

    def __str__(self):
        if self.user.get_full_name() != None:
            return self.user.get_full_name()
        else:
            return "NOT CREATE"


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
    mobile_number = models.CharField(
        "Contact Number (+91xxxxxxxxxx)",
        validators=[phone_regex],
        max_length=15,
        blank=True,
    )
    mci_registeration_number = models.CharField(
        "Medical Counsel of India Registration Number",
        max_length=50,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.hospital_name:
            return self.hospital_name
        else:
            return "NOT CREATE"


@receiver(post_save, sender=User)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "DONOR":
            profile = DonorProfile.objects.create(user=instance)
        else:
            profile = HospitalProfile.objects.create(user=instance)

        profile.save()
