from django.contrib import admin

from table.models import Limit, LimitItem, Site


class LimitModelAdmin(admin.ModelAdmin):

    def save_related(self, request, form, formsets, change):
        super(LimitModelAdmin, self).save_related(request, form, formsets, change)

        for site in Site.objects.all():
            limit_item = LimitItem.objects.create(site=site)
            form.instance.item.add(limit_item)


class SiteModelAdmin(admin.ModelAdmin):

    def save_related(self, request, form, formsets, change):
        super(SiteModelAdmin, self).save_related(request, form, formsets, change)

        # новому сайту добавляем итемы лимитов
        for limit in Limit.objects.all():
            new_item = LimitItem.objects.create(site=form.instance)
            limit.item.add(new_item)


admin.site.register(Limit, LimitModelAdmin)
admin.site.register(LimitItem)
admin.site.register(Site, SiteModelAdmin)
