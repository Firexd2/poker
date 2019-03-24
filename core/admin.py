from django.contrib import admin
from django.contrib.admin import AdminSite

from core.admin_forms import TranslationsModelForm, ContactModelForm
from core.models import Translation, Contact
from table.models import Limit, LimitItem, Site, Table, PriceFormation, StatisticLimitItem


class CustomAdmin(AdminSite):

    site_title = 'Administration'
    site_header = 'Poker stat administration'
    index_title = 'Management'

    def get_app_list(self, request):
        # порядок, в котором будут отображаться модели
        _order = (
            Table._meta.verbose_name_plural,
            Site._meta.verbose_name_plural,
            Limit._meta.verbose_name_plural,
            LimitItem._meta.verbose_name_plural,
            StatisticLimitItem._meta.verbose_name_plural,
            PriceFormation._meta.verbose_name_plural
        )
        order_rank = {key_val.lower(): rank for rank, key_val in enumerate(_order)}

        app_list = super(CustomAdmin, self).get_app_list(request)

        for app in app_list:
            if app['name'] == 'Table':
                app['models'].sort(key=lambda val: order_rank[val['name'].lower()])

        return app_list


admin_site = CustomAdmin()
admin_site.disable_action('delete_selected')


@admin.register(Translation, site=admin_site)
class TranslationsModelAdmin(admin.ModelAdmin):
    form = TranslationsModelForm


@admin.register(Contact, site=admin_site)
class ContactModelAdmin(admin.ModelAdmin):
    form = ContactModelForm
