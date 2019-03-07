from django.contrib import admin

from core.mixins.admin.forms import ModelAdminFieldSetsMixin
from core.mixins.utils.mixins import make_enabled, make_disabled
from table.admin_forms import LimitModelForm, SiteModelForm
from table.models import Limit, LimitItem, Site, Table

admin.site.disable_action('delete_selected')


@admin.register(Limit)
class LimitModelAdmin(ModelAdminFieldSetsMixin, admin.ModelAdmin):
    form = LimitModelForm

    def save_related(self, request, form, formsets, change):
        super(LimitModelAdmin, self).save_related(request, form, formsets, change)

        if not change:
            table = form.cleaned_data['table']
            # привязываем к таблице новый limit
            table.limits.add(form.instance)

            for site in Site.objects.filter(limititem__limit__table=table).distinct():
                limit_item = LimitItem.objects.create(site=site)
                form.instance.items.add(limit_item)

            # для просчета приорити
            form.instance.save()


@admin.register(Site)
class SiteModelAdmin(ModelAdminFieldSetsMixin, admin.ModelAdmin):
    form = SiteModelForm

    # TODO: решить проблему, когда при редактировании объекта выскакивает ошибку

    def save_related(self, request, form, formsets, change):
        super(SiteModelAdmin, self).save_related(request, form, formsets, change)

        if not change:
            table = form.cleaned_data['table']

            # новому сайту добавляем итемы лимитов
            for limit in Limit.objects.filter(table=table):
                new_item = LimitItem.objects.create(site=form.instance)
                limit.items.add(new_item)

            # для просчета приорити
            form.instance.save()


@admin.register(LimitItem)
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


@admin.register(Table)
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
