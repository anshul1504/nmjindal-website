from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this, simple bots do.
    website_url = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off", "aria-hidden": "true",
    }))

    class Meta:
        model = Enquiry
        fields = ["name", "company", "email", "phone", "interest", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "company": forms.TextInput(attrs={"placeholder": "Company (optional)", "autocomplete": "organization"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone / WhatsApp (optional)", "autocomplete": "tel"}),
            "interest": forms.Select(),
            "message": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Tell us what you want to buy or sell: product, quantity, destination and timeline.",
            }),
        }

    def clean_website_url(self):
        if self.cleaned_data.get("website_url"):
            raise forms.ValidationError("Spam detected.")
        return ""
