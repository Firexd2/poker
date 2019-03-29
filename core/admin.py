from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite

from core.admin_forms import TranslationsModelForm, ContactModelForm, EmailBackendSettingModelForm
from core.models import Translation, Contact, EmailBackendSetting
from core.tools.mixins.admin import DeletePriorityFieldForCreateMixin
from table.models import Limit, LimitItem, Site, Table, PriceFormation, StatisticLimitItem


class CustomAdmin(AdminSite):

    site_title = 'Administration'
    site_header = 'Poker stat administration'
    index_title = 'Management'

    def get_app_list(self, request):
        # порядок, в котором будут отображаться модели
        _order_for_table = (
            Table._meta.verbose_name_plural,
            Site._meta.verbose_name_plural,
            Limit._meta.verbose_name_plural,
            LimitItem._meta.verbose_name_plural,
            StatisticLimitItem._meta.verbose_name_plural,
            PriceFormation._meta.verbose_name_plural
        )
        order_rank_for_table = {key_val.lower(): rank for rank, key_val in enumerate(_order_for_table)}

        app_list = super(CustomAdmin, self).get_app_list(request)

        for app in app_list:
            if app['name'] == 'Table':
                app['models'].sort(key=lambda val: order_rank_for_table[val['name'].lower()])

        return app_list


admin_site = CustomAdmin()
admin_site.disable_action('delete_selected')


@admin.register(Translation, site=admin_site)
class TranslationsModelAdmin(DeletePriorityFieldForCreateMixin, admin.ModelAdmin):
    form = TranslationsModelForm

    list_display = ('__str__', 'image', 'default')

    # поля, которым виджет на TextInput менять НЕ НАДО
    exclude_names_field = (
        'some_text_in_block', 'text_in_about', 'text_in_sales', 'text_in_articles', 'text_in_faq',
        'text_in_instruction', 'success', 'priority', 'default', 'image', 'email_letter_body_for_client',
        'email_letter_body_for_admin'
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(TranslationsModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name not in self.exclude_names_field and formfield:
            formfield.widget = forms.TextInput(attrs=formfield.widget.attrs)
        return formfield

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.default:
            return ('default',)
        else:
            return super(TranslationsModelAdmin, self).get_readonly_fields(request, obj)


@admin.register(Contact, site=admin_site)
class ContactModelAdmin(DeletePriorityFieldForCreateMixin, admin.ModelAdmin):
    form = ContactModelForm

    list_display = ('__str__', 'details')


@admin.register(EmailBackendSetting, site=admin_site)
class EmailBackendSettingModelAdmin(admin.ModelAdmin):
    form = EmailBackendSettingModelForm

    list_display = ('host_user', 'is_active')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_active:
            return ('is_active',)
        else:
            return super(EmailBackendSettingModelAdmin, self).get_readonly_fields(request, obj)
