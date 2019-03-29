from django import forms
from order.models import Order, TypePayment


class OrderForm(forms.ModelForm):
    type_payment_qs = TypePayment.objects.filter(is_enabled=True)

    payment = forms.ModelChoiceField(queryset=type_payment_qs, widget=forms.RadioSelect(), empty_label=None)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    limit_items = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = ('payment', 'email', 'name', 'limit_items')
