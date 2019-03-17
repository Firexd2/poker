from django.contrib import admin
from django.contrib.admin import AdminSite

from core.tools.mixins.admin import ModelAdminFieldSetsMixin
from core.tools.utils import make_enabled, make_disabled
from table.admin_forms import LimitModelForm, SiteModelForm, StatisticLimitModelForm
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
            app['models'].sort(key=lambda val: order_rank[val['name'].lower()])

        return app_list


admin_site = CustomAdmin()
admin_site.disable_action('delete_selected')


@admin.register(Limit, site=admin_site)
class LimitModelAdmin(ModelAdminFieldSetsMixin, admin.ModelAdmin):
    form = LimitModelForm

    def save_related(self, request, form, formsets, change):
        super(LimitModelAdmin, self).save_related(request, form, formsets, change)

        if not change:
            table = form.cleaned_data['table']
            # привязываем к таблице новый limit
            table.limits.add(form.instance)

            for site in Site.objects.filter(limititem__limit__table=table):
                stat = StatisticLimitItem.objects.create()
                new_item = LimitItem.objects.create(site=site, stat=stat)
                form.instance.items.add(new_item)

            # для просчета приорити
            form.instance.save()

    def delete_model(self, request, obj):
        # сохраняем ids, так как из-за ленивости queryset'а после удаления объекта он здесь будет пустой
        limit_items_ids = [item.id for item in obj.items.all()]
        stat_ids = [item.stat.id for item in obj.items.all()]
        super(LimitModelAdmin, self).delete_model(request, obj)

        StatisticLimitItem.objects.filter(id__in=stat_ids).delete()
        LimitItem.objects.filter(id__in=limit_items_ids).delete()


@admin.register(Site, site=admin_site)
class SiteModelAdmin(ModelAdminFieldSetsMixin, admin.ModelAdmin):
    form = SiteModelForm

    def save_related(self, request, form, formsets, change):
        super(SiteModelAdmin, self).save_related(request, form, formsets, change)

        if not change:
            table = form.cleaned_data['table']

            # новому сайту добавляем итемы лимитов
            for limit in Limit.objects.filter(table=table):
                stat = StatisticLimitItem.objects.create()
                new_item = LimitItem.objects.create(site=form.instance, stat=stat)
                limit.items.add(new_item)

            # для просчета приорити
            form.instance.save()

    def delete_model(self, request, obj):
        limits_items = obj._get_limits_items()
        stat_ids = [item.stat.id for item in limits_items]
        super(SiteModelAdmin, self).delete_model(request, obj)

        StatisticLimitItem.objects.filter(id__in=stat_ids).delete()
        limits_items.delete()


@admin.register(LimitItem, site=admin_site)
class LimitItemAdmin(admin.ModelAdmin):
    actions = [make_enabled, make_disabled]

    fieldsets = (
        (None, {
            'fields': ('is_enabled', 'price_per_month', 'price_per_100k'),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StatisticLimitItem, site=admin_site)
class StatisticLimitItemAdmin(admin.ModelAdmin):
    form = StatisticLimitModelForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Table, site=admin_site)
class TableAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'is_enabled', 'priority'),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PriceFormation, site=admin_site)
class PriceFormationAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
