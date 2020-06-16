from django.core.validators import RegexValidator


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [
        ".pdf",
    ]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Please attach a pdf file")


phone_regex = RegexValidator(
    regex=r"^\+?91?\d{9,10}$",
    message="Phone number must be entered in the format: '+91xxxxxxxxxx'. Up to 9-10 digits allowed.",
)
