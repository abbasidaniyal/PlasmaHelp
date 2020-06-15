from django.db import models

from profiles.validators import phone_regex


class Query(models.Model):

    name = models.CharField("Name", max_length=50, null=False)
    email = models.EmailField("email address", null=False)
    contact_number = models.CharField(
        "Contact Number (+91xxxxxxxxxx)",
        validators=[phone_regex],
        max_length=15,
        blank=True,
    )
    query = models.TextField("Query", max_length=200, blank=False)
    date = models.DateTimeField("Recorded at ", editable=False, auto_now=True)

    def __str__(self):
        return self.name + " : " + self.query[:50]
