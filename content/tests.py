from django.shortcuts import reverse
from django.test import tag, SimpleTestCase
from django.urls import resolve

from content.forms import QueryForm
from content.views import home_page, QueryPageView, faq_page, privacy_policy


# class DecoratorTest(TestCase):
#     def setUp(self) -> None:
#         # with open('temp.pdf','w') as f1, open('temp2.pdf','w') as f2:
#         #     self.donor_profile = DonorProfile.objects.create(
#         #         first_name='foo', last_name='bar',
#         #         mobile_number='+919999999999',
#         #         birth_date=date(year=2000, month=1, day=1),
#         #         location=Point(10, 20),
#         #         date_last_tested_negative=date(year=2020, month=1, day=1),
#         #         last_covid_report=f1,
#         #         igg_report=f2
#         #     )
#         pass
#         # self.hospital_profile = HospitalProfile.objects.create(
#         #     hospital_name='FOO', hospital_address="BAR", contact_person_name='foo bar',
#         #     contact_person_mobile_number='+911111111111', mci_registration_number="xxxxxxxx", location=Point(10, 10),
#         # )
#
#     @tag('this')
#     def test_donor_complete(self):
#         self.client = Client()
#         self.user = User.objects.create(email='donor@donor.com', user_type='DONOR')
#         self.client.force_login(User.objects.get(email='donor@donor.com'))
#         file = SimpleUploadedFile(
#             "best_file_eva.pdf",
#             b"these are the file contents!"
#         )
#         self.donor_profile = DonorProfile.objects.create(
#             first_name='foo', last_name='bar',
#             mobile_number='+919999999999',
#             birth_date=date(year=2000, month=1, day=1),
#             location=Point(10, 20),
#             date_last_tested_negative=date(year=2020, month=1, day=1),
#             last_covid_report=file,
#             igg_report=file,
#             user=self.user
#         )
#
#         request = self.client.get('/foo', follow=True)
#         request.user = self.user
#         res = profile_incomplete_check(lambda request: HttpResponse(request))(request)
#         import ipdb;
#         ipdb.set_trace()
#         print(res.context['messages'])


class ContentFormTest(SimpleTestCase):
    def setUp(self) -> None:
        self.form = QueryForm

    def test_fields(self):
        self.assertEqual(
            list(self.form().fields.keys()),
            ["name", "email", "contact_number", "query"],
        )

    def test_placeholder_and_class(self):
        for _, value in self.form().fields.items():
            if value.required:
                self.assertEqual(value.widget.attrs["placeholder"], value.label + "*")
            else:
                self.assertEqual(value.widget.attrs["placeholder"], value.label)

            self.assertEqual(value.widget.attrs["class"], "textbox")


class ContentURLTest(SimpleTestCase):
    @tag("urls")
    def test_home_page_url(self):
        url = reverse("home-page")

        self.assertEqual(url, "/")
        self.assertEqual(resolve(url).func, home_page)

    @tag("urls")
    def test_query_page_url(self):
        url = reverse("query")

        self.assertEqual(url, "/query/")
        self.assertEqual(resolve(url).func.view_class, QueryPageView)

    @tag("urls")
    def test_faq_page_url(self):
        url = reverse("faq")

        self.assertEqual(url, "/faqs/")
        self.assertEqual(resolve(url).func, faq_page)

    @tag("urls")
    def test_privacy_policy_page_url(self):
        url = reverse("privacy-policy")

        self.assertEqual(url, "/privacy_policy/")
        self.assertEqual(resolve(url).func, privacy_policy)
