from django import forms

from table.models import Table


class ModelAdminFieldSetsMixin:
    """Миксин для кастомизации fieldsets
    """
    def get_fieldsets(self, request, obj=None):
        if obj:
            fieldsets = (
                (None, {
                    'fields': ('name', 'is_enabled', 'priority'),
                }),
            )
        else:
            fieldsets = (
                ('Which table to add at?', {
                    'fields': ('table',),
                }),
                (None, {
                    'fields': ('name', 'is_enabled'),
                })
            )

        return fieldsets


class ModelFormTableMixin(forms.ModelForm):
    """Миксин для добавления кастомного поля table для форм в админке
    """
    table = forms.ModelChoiceField(queryset=Table.objects.order_by('name'), required=True)
    name = forms.CharField(required=True)
    priority = forms.IntegerField(required=True, min_value=1)

    def __init__(self, *args, **kwargs):
        super(ModelFormTableMixin, self).__init__(*args, **kwargs)

        # при редактировании таблицу не трогаем
        if kwargs.get('instance'):
            self.fields['table'].required = False
        else:
            # при создании priority - нет в форме
            self.fields['priority'].required = False
