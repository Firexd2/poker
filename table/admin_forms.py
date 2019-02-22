from django import forms

from core.mixins.admin.forms import ModelFormTableMixin
from table.models import Limit, Site, Table


class LimitModelForm(ModelFormTableMixin, forms.ModelForm):

    class Meta:
        model = Limit
        exclude = []


class SiteModelForm(ModelFormTableMixin, forms.ModelForm):

    class Meta:
        model = Site
        exclude = []
