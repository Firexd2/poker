from django.contrib import admin
from django.utils.safestring import mark_safe

from core.admin import admin_site
from .admin_forms import OrderModelForm, TypePaymentModelForm
from order.models import Order, TypePayment, OrderItem


class OrderItemInstanceInline(admin.TabularInline):
    # добавляем в __str__ js скрипт, который приведет inline шаблон к оптимальному виду
    Order.items.through.__str__ = lambda x: mark_safe(
        """
        <script id="script">document.getElementById("script").parentElement.style.display = "none";
        document.addEventListener('DOMContentLoaded', function() {
            var elems = document.getElementsByClassName("field-orderitem")
                for (var i=0; i<elems.length;i++) {
                    elems[i].style.paddingTop = '5px'
                };
            }
        );
        </script>
        """
    )
    model = Order.items.through

    readonly_fields = ('orderitem',)
    verbose_name = 'Item'
    verbose_name_plural = 'Order items'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    form = OrderModelForm
    readonly_fields = ('total_price', 'name', 'email', 'payment', 'notes')
    exclude = ('items',)
    inlines = [OrderItemInstanceInline]


@admin.register(TypePayment, site=admin_site)
class TypePaymentModelAdmin(admin.ModelAdmin):
    form = TypePaymentModelForm

    list_display = ('__str__', 'payment_details', 'is_enabled')
