from django import forms

from table.models import Table


class DeleteTableFieldForCreateSetsMixin:
    """При редактировании объекта убираем table из списка филдов
    """
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(DeleteTableFieldForCreateSetsMixin, self).get_fieldsets(request, obj)
        if obj:
            fields = fieldsets[0][1]['fields']
            # при редактировании table убираем
            del fields[fields.index('table')]

        return fieldsets


class DeletePriorityFieldForCreateMixin:
    """При создании объекта убираем priority из списка филдов
    """
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(DeletePriorityFieldForCreateMixin, self).get_fieldsets(request, obj)
        if not obj:
            fields = fieldsets[0][1]['fields']
            # при редактировании table убираем
            del fields[fields.index('priority')]

        return fieldsets


class TableMixin(forms.ModelForm):
    """Миксин для добавления кастомного поля table для форм в админке
    """
    table = forms.ModelChoiceField(queryset=Table.objects.order_by('name'), required=True)
    name = forms.CharField(required=True)
    priority = forms.IntegerField(required=True, min_value=1)

    def __init__(self, *args, **kwargs):
        super(TableMixin, self).__init__(*args, **kwargs)

        # при редактировании таблицу не трогаем
        if kwargs.get('instance'):
            self.fields['table'].required = False
        else:
            # при создании priority - нет в форме
            self.fields['priority'].required = False
