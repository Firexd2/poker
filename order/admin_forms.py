from django import forms

from order.models import Order


class OrderModelForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = []


class TypePaymentModelForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput)
    payment_details = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Order
        exclude = []
