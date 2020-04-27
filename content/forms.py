from django import forms

from content.models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ("name", "email", "contact_number", "query")
