from django.urls import path

from content.views import home_page, QueryPageView, faq_page

urlpatterns = [
    path("", home_page, name="home-page"),
    path("query/", QueryPageView.as_view(), name="query"),
    path("faqs/", faq_page, name="faq"),
]
