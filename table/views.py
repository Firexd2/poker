from django.http import HttpResponse
from django.views.generic import TemplateView

from table.models import Limit, Site, Table, LimitItem


class TableView(TemplateView):
    template_name = 'table/home.html'

    def get_context_data(self, **kwargs):
        context = super(TableView, self).get_context_data()

        tables = Table.objects.filter(is_enabled=True)
        type_table = self.request.GET.get('table', tables.first().name_url)

        limits = Limit.objects.filter(is_enabled=True, table__name_url=type_table)

        context['sites'] = Site.objects.filter(limititem__limit__table__name_url=type_table)
        context['limits'] = limits
        context['tables'] = tables
        return context

    def _add_to_cart(self):
        """Добавляет в корзину (по сути в куки) новый объект
        """
        data = self.request.POST.copy()
        data['price'] = self._calculate_order()
        data['limits_item'] = self._get_dict_limits_items()

        if 'cart_items' not in self.request.session:
            self.request.session['cart_items'] = [data]
        else:
            cart_items = self.request.session['cart_items']
            cart_items.append(data)
            self.request.session['cart_items'] = cart_items

        # расчитываем общую сумму корзины
        self.request.session['total'] = sum(item['price'] for item in self.request.session['cart_items'])

    def _get_dict_limits_items(self):
        limit_items_ids = self.request.POST.getlist('limit_items_ids[]')

        result = {}
        for limit_item in LimitItem.objects.filter(id__in=limit_items_ids):
            if not limit_item.site.name in result:
                result[limit_item.site.name] = []

            result[limit_item.site.name].append(limit_item._get_limit().name)

        # преобразуем название лимитов из списка в строку
        for key in result:
            result[key] = ", ".join(result[key])
        return result

    def _calculate_order(self):
        return 100

    def post(self, *args, **kwargs):

        self._add_to_cart()

        return HttpResponse()
