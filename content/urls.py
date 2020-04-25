from django.urls import path, include

from content.views import home_page, QueryPageView, FAQView

urlpatterns = [
    path("", home_page, name="home-page"),
    path("query/", QueryPageView.as_view(), name="query"),
    path("faqs/", FAQView.as_view(), name="faq"),
]
