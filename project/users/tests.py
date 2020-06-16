from django.contrib.auth import views as django_views
from django.shortcuts import reverse
from django.test import SimpleTestCase, tag
from django.urls import resolve

import users.views as views


class URLTest(SimpleTestCase):
    def setUp(self) -> None:
        self.base_url = "/users/"

    @tag("urls")
    def test_login_page_url(self):
        url = reverse("login")
        self.assertEqual(url, self.base_url + "login/")
        self.assertEqual(resolve(url).func.view_class, views.LoginPageView)

    @tag("urls")
    def test_home_page_url(self):
        url = reverse("logout")
        self.assertEqual(url, self.base_url + "logout/")
        self.assertEqual(resolve(url).func.view_class, views.LogoutPageView)

    @tag("urls")
    def test_register_donor_page_url(self):
        url = reverse("register-donor")
        self.assertEqual(url, self.base_url + "register_donor/")
        self.assertEqual(resolve(url).func.view_class, views.DonorRegisterView)

    @tag("urls")
    def test_register_patient_page_url(self):
        url = reverse("register-patient")
        self.assertEqual(url, self.base_url + "register_patient/")
        self.assertEqual(resolve(url).func.view_class, views.PatientRegisterView)

    @tag("urls")
    def test_register_hospital_url(self):
        url = reverse("register-hospital")
        self.assertEqual(url, self.base_url + "register_hospital/")
        self.assertEqual(resolve(url).func.view_class, views.HospitalRegisterView)

    @tag("urls")
    def test_delete_user_page_url(self):
        url = reverse("delete-user")
        self.assertEqual(url, self.base_url + "profile/delete/")
        self.assertEqual(resolve(url).func.view_class, views.DeleteUserView)

    @tag("urls")
    def test_activate_page_url(self):
        url = reverse("activate", args=["xxx", "yyy"])
        self.assertEqual(url, self.base_url + "activate/xxx/yyy/")
        self.assertEqual(resolve(url).func, views.activate)

    @tag("urls")
    def test_resend_verification_link_page_url(self):
        url = reverse("resend-verification")
        self.assertEqual(url, self.base_url + "resend_verification_link/")
        self.assertEqual(resolve(url).func.view_class, views.ResendVerification)

    @tag("urls")
    def test_password_change_page_url(self):
        url = reverse("password_change")
        self.assertEqual(url, self.base_url + "password_change/")
        self.assertEqual(resolve(url).func.view_class, views.CustomPasswordChangeView)

    @tag("urls")
    def test_password_change_done_page_url(self):
        url = reverse("password_change_done")
        self.assertEqual(url, self.base_url + "password_change/done/")
        self.assertEqual(
            resolve(url).func.view_class, django_views.PasswordChangeDoneView
        )

    @tag("urls")
    def test_password_reset_page_url(self):
        url = reverse("password_reset")
        self.assertEqual(url, self.base_url + "password_reset/")
        self.assertEqual(resolve(url).func.view_class, views.CustomPasswordResetView)

    @tag("urls")
    def test_password_reset_done_page_url(self):
        url = reverse("password_reset_done")
        self.assertEqual(url, self.base_url + "password_reset/done/")
        self.assertEqual(
            resolve(url).func.view_class, django_views.PasswordResetDoneView
        )

    @tag("urls")
    def test_password_reset_confirm_page_url(self):
        url = reverse("password_reset_confirm", args=["xxx", "yyy"])
        self.assertEqual(url, self.base_url + "reset/xxx/yyy/")
        self.assertEqual(
            resolve(url).func.view_class, django_views.PasswordResetConfirmView
        )

    @tag("urls")
    def test_password_reset_complete_page_url(self):
        url = reverse("password_reset_complete")
        self.assertEqual(url, self.base_url + "reset/done/")
        self.assertEqual(
            resolve(url).func.view_class, django_views.PasswordResetCompleteView
        )
