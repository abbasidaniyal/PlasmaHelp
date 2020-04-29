from django import forms

from content.models import Query


class QueryForm(forms.ModelForm):
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
        model = Query
        fields = ("name", "email", "contact_number", "query")
