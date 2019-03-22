from django.contrib import admin

from core.admin import admin_site
from core.admin_form import OrderModelForm
from order.models import Order


@admin.register(Order, site=admin_site)
class LimitModelAdmin(admin.ModelAdmin):
    form = OrderModelForm
