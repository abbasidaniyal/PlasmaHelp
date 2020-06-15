from django import forms
from mapwidgets.widgets import GooglePointFieldWidget
from profiles.models import DonorProfile, HospitalProfile


class MyDateInput(forms.DateInput):
    input_type = "date"


class DonorProfileCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"

    class Meta:
        model = DonorProfile

        fields = (
            "first_name",
            "last_name",
            "mobile_number",
            "birth_date",
            "location",
            "date_last_tested_negative",
            "last_covid_report",
            "igg_report",
        )
        widgets = {
            "birth_date": MyDateInput(
                attrs={"class": "textbox", "placeholder": "Date of Birth"}
            ),
            "date_last_tested_negative": MyDateInput(
                attrs={
                    "class": "textbox",
                    "placeholder": "Date Last COVID19 Negative Test Report",
                }
            ),
            "location": GooglePointFieldWidget(),
        }


class HospitalProfileCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"

    class Meta:
        model = HospitalProfile
        fields = (
            "hospital_name",
            "hospital_address",
            "contact_person_name",
            "contact_person_mobile_number",
            "mci_registration_number",
            "location",
        )
        widgets = {
            "location": GooglePointFieldWidget(),
        }


class DonorProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"

    class Meta:
        model = DonorProfile

        fields = (
            "mobile_number",
            "location",
            "date_last_tested_negative",
            "last_covid_report",
            "igg_report",
        )
        widgets = {
            "date_last_tested_negative": MyDateInput(
                attrs={
                    "class": "textbox",
                    "placeholder": "Date Last COVID19 Negative Test Report",
                }
            ),
            "location": GooglePointFieldWidget(),
        }


class HospitalProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"

    class Meta:
        model = HospitalProfile
        fields = (
            "contact_person_name",
            "contact_person_mobile_number",
            "location",
        )
        widgets = {
            "location": GooglePointFieldWidget(),
        }
