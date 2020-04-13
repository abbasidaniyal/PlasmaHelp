from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import DonorProfile, HospitalProfile,User

class DateInput(forms.DateInput):
    input_type = 'date'

class DonorUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2','first_name','last_name',)


class DonorProfileForm(forms.ModelForm):

    class Meta:
        model = DonorProfile

        fields = ('mobile_number', 'birth_date', 'location', 'report')
        widgets = {
            'birth_date': DateInput(),
        }


class HospitalUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2','first_name','last_name',)

class HospitalProfileForm(forms.ModelForm):
    class Meta:
        model = HospitalProfile
        fields = ('hospital_name','hospital_address','mobile_number','mci_registeration_number','location',)