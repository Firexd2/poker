from django import forms

from core.models import Translation, Contact


class TranslationsModelForm(forms.ModelForm):

    class Meta:
        model = Translation
        exclude = []


class ContactModelForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = []
