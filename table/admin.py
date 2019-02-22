from django.contrib import admin

from core.mixins.admin.forms import ModelAdminFieldSetsMixin
from table.admin_forms import LimitModelForm, SiteModelForm
from table.models import Limit, LimitItem, Site, Table


@admin.register(Limit)
class LimitModelAdmin(ModelAdminFieldSetsMixin, admin.ModelAdmin):
    form = LimitModelForm

    def save_related(self, request, form, formsets, change):
        super(LimitModelAdmin, self).save_related(request, form, formsets, change)

        table = form.cleaned_data['table']
        # привязываем к таблице новый limit
        table.limit.add(form.instance)

        for site in Site.objects.filter(limititem__limit__table=table).distinct():
            limit_item = LimitItem.objects.create(site=site)
            form.instance.item.add(limit_item)


@admin.register(Site)
class SiteModelAdmin(ModelAdminFieldSetsMixin, admin.ModelAdmin):
    form = SiteModelForm

    def save_related(self, request, form, formsets, change):
        super(SiteModelAdmin, self).save_related(request, form, formsets, change)

        table = form.cleaned_data['table']

        # новому сайту добавляем итемы лимитов
        for limit in Limit.objects.filter(table=table):
            new_item = LimitItem.objects.create(site=form.instance)
            limit.item.add(new_item)


admin.site.register(LimitItem)
admin.site.register(Table)
