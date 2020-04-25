from django import forms
from django.contrib.auth.forms import UserCreationForm
from mapwidgets.widgets import GooglePointFieldWidget

from users.models import DonorProfile, HospitalProfile, User


class DateInput(forms.DateInput):
    input_type = "date"


class DonorUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = User(
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            is_active=False,
        )
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "DONOR"
        if commit:
            user.save()
        return user


class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile

        fields = ("mobile_number", "birth_date", "location", "report")
        widgets = {
            "birth_date": DateInput(),
            "location": GooglePointFieldWidget(),
        }


class HospitalUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = User(email=self.cleaned_data["email"], is_active=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "HOSPITAL"
        if commit:
            user.save()
        return user


class HospitalProfileForm(forms.ModelForm):
    class Meta:
        model = HospitalProfile
        fields = (
            "hospital_name",
            "hospital_address",
            "mobile_number",
            "mci_registeration_number",
            "location",
        )
        widgets = {"location": GooglePointFieldWidget()}
