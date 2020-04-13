from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField

from users.validators import validate_file_extension, validate_mobile_number
from users.managers import CustomUserManager

from plasma_for_covid import settings


class User(AbstractUser):
    
    user_options = [("DONOR", "Donor"), ("HOSPITAL", "Hospital")]
    user_type = models.CharField(max_length=20, choices=user_options)
    email = models.EmailField('email address', unique=True, blank=False, null=False)
    username = None

    USERNAME_FIELD = 'email'
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=False, null=False)
    birth_date = models.DateField(null=False, blank=False)
    mobile_number = PhoneField(blank=True, help_text='Contact Number', validators=[validate_mobile_number])
    report = models.FileField(null=False, blank=False, validators=[validate_file_extension])


class HospitalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100, blank=False, null=False)
    hospital_address = models.TextField(max_length=500, blank=False, null=False)
    location = models.CharField(max_length=30, blank=False)
    mobile_number = PhoneField(blank=False, help_text='Contact Number')
    mci_registeration_number = models.CharField(max_length=50, blank=False, null=False)
