from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView

from content.forms import QueryForm
from content.decorators import profile_incomplete_check
from content.utils import send_query


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
