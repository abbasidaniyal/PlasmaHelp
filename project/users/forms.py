from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    authenticate,
    UsernameField,
    PasswordChangeForm,
    PasswordResetForm,
)

from users.models import User


class MyDateInput(forms.DateInput):
    input_type = "date"


class DonorUserForm(UserCreationForm):
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
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = User(
            email=self.cleaned_data["email"], password=self.cleaned_data["password1"],
        )
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "DONOR"
        if commit:
            user.save()
        return user


class PatientUserForm(UserCreationForm):
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
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = User(
            email=self.cleaned_data["email"], password=self.cleaned_data["password1"],
        )
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "PATIENT"
        if commit:
            user.save()
        return user


class HospitalUserForm(UserCreationForm):
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
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = User(email=self.cleaned_data["email"])
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "HOSPITAL"
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Email", "class": "textbox"}
        )
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Password",
                "class": "textbox",
            }
        ),
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            if username is not None and password:
                self.user_cache = authenticate(
                    self.request, username=username, password=password
                )
                if self.user_cache is None:
                    try:
                        user_temp = User.objects.get(email=username)
                    except:
                        user_temp = None

                    if user_temp is not None:
                        self.confirm_login_allowed(user_temp)
                    else:
                        raise forms.ValidationError(
                            self.error_messages["invalid_login"],
                            code="invalid_login",
                            params={"username": self.username_field.verbose_name},
                        )
        except Exception as e:
            raise e
        return self.cleaned_data


class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "textbox", "placeholder": "Email"}),
    )


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "textbox", "placeholder": "Email"}),
    )


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"
