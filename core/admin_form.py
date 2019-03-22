from django import forms

from order.models import Order


class OrderModelForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = []
