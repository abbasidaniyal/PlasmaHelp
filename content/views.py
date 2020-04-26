from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView

from content.forms import QueryForm


def send_query(request, object):
    pass


def home_page(request):
    return render(request, "index.html")


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
