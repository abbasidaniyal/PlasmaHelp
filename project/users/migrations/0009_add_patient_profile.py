# Generated by Django 3.0.7 on 2020-06-16 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_refactored_profiles_to_separate_app"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("DONOR", "Donor"),
                    ("HOSPITAL", "Hospital"),
                    ("PATIENT", "Patient"),
                    ("STAFF", "Staff"),
                ],
                max_length=20,
            ),
        ),
    ]
