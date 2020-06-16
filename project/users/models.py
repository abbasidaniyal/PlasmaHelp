from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class User(AbstractUser):
    user_options = [
        ("DONOR", "Donor"),
        ("HOSPITAL", "Hospital"),
        ("PATIENT", "Patient"),
        ("STAFF", "Staff"),
    ]
    user_type = models.CharField(
        max_length=20, choices=user_options, null=False, blank=False
    )
    email = models.EmailField("email address", unique=True)
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=False)
    objects = CustomUserManager()

    def __str__(self):
        return self.email
