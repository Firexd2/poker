from django.contrib import admin

from core.admin import admin_site
from core.tools.mixins.admin import DeleteTableFieldForCreateSetsMixin, DeletePriorityFieldForCreateMixin
from core.tools.utils import make_enabled, make_disabled
from table.admin_forms import LimitModelForm, SiteModelForm, StatisticLimitModelForm
from table.models import Limit, LimitItem, Site, Table, PriceFormation, StatisticLimitItem


@admin.register(Limit, site=admin_site)
class LimitModelAdmin(DeleteTableFieldForCreateSetsMixin, DeletePriorityFieldForCreateMixin, admin.ModelAdmin):
    form = LimitModelForm

    list_display = ('__str__', 'is_enabled')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(LimitModelAdmin, self).get_fieldsets(request, obj)
        fields = fieldsets[0][1]['fields']

        del fields[fields.index('items')]

        return fieldsets

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
class SiteModelAdmin(DeleteTableFieldForCreateSetsMixin, DeletePriorityFieldForCreateMixin, admin.ModelAdmin):
    form = SiteModelForm

    list_display = ('__str__', 'is_enabled')

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

    list_display = ('__str__', 'price_per_month', 'price_per_100k', 'is_enabled')

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

    list_display = ('__str__', 'min_value', 'max_value')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Table, site=admin_site)
class TableAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'is_enabled')

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
