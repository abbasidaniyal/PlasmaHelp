# Generated by Django 3.0.7 on 2020-06-16 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_add_patient_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="patientprofile",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]