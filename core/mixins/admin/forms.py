from django import forms

from table.models import Table


class ModelAdminFieldSetsMixin:
    """Миксин для кастомизации fieldsets
    """
    def get_fieldsets(self, request, obj=None):
        if obj:
            fieldsets = (
                (None, {
                    'fields': ('name', 'is_enabled',),
                }),
            )
        else:
            fieldsets = (
                ('Which table to add at?', {
                    'fields': ('table',),
                }),
                (None, {
                    'fields': ('name', 'is_enabled',),
                })
            )

        return fieldsets


class ModelFormTableMixin(forms.ModelForm):
    """Миксин для добавления кастомного поля table для форм в админке
    """
    table = forms.ModelChoiceField(queryset=Table.objects.order_by('name'))
    name = forms.CharField(required=True)
