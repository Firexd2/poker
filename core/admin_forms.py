from django import forms

from core.models import Translation, Contact, EmailBackendSetting


class TranslationsModelForm(forms.ModelForm):

    class Meta:
        model = Translation
        exclude = []

    def clean(self):
        cleaned_data = super(TranslationsModelForm, self).clean()

        email_letter_body_for_client = cleaned_data.get('email_letter_body_for_client')
        if email_letter_body_for_client:
            for key in Translation.required_keys_for_client:
                if key not in email_letter_body_for_client:
                    self.add_error('email_letter_body_for_client', 'Required: ' + ', '.join(Translation.required_keys_for_client))

        email_letter_body_for_admin = cleaned_data.get('email_letter_body_for_admin')
        if email_letter_body_for_admin:
            for key in Translation.required_keys_for_admin:
                if key not in email_letter_body_for_admin:
                    self.add_error('email_letter_body_for_admin', 'Required: ' + ', '.join(Translation.required_keys_for_admin))

        name = cleaned_data.get('name')
        if not name:
            self.add_error('name', 'Name is required.')

        return cleaned_data


class ContactModelForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput)
    details = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Contact
        exclude = []


class EmailBackendSettingModelForm(forms.ModelForm):

    class Meta:
        model = EmailBackendSetting
        exclude = []
