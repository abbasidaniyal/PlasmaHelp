from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView

from users.utils import send_mail

from content.forms import QueryForm
from plasma_for_covid import settings
from datetime import datetime

from content.decorators import profile_incomplete_check


def send_query(request, query):
    send_mail(
        "A new query from PlasmaHelp Website",
        f"""
Name : {query.name}
Email : {query.email}
Contact Number : {query.contact_number}
DateTime : {datetime.now()} UTC
Query : {query.query}
        """,
        f"{query.email}",
        [f"{settings.EMAIL_HOST_USER}"],
        fail_silently=True,
    )


@profile_incomplete_check
def privacy_policy(request):
    return render(request, "privacy_policy.html")


@profile_incomplete_check
def home_page(request):
    return render(request, "index.html")


@profile_incomplete_check
def faq_page(request):
    return render(request, "content/faqs.html")


class QueryPageView(SuccessMessageMixin, CreateView):
    form_class = QueryForm
    template_name = "content/query_page.html"
    success_url = "/"
    success_message = "Your feedback has been recorded. We will get back to you ASAP!"

    def form_valid(self, form):
        response = super().form_valid(form)

        send_query(self.request, self.object)
        return response
