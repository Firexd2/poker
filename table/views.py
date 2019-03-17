import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from table.models import Limit, Site, Table, LimitItem, PriceFormation, StatisticLimitItem
from table.admin_forms import StatisticLimitModelForm


# TODO: рефакторинг
class TableView(TemplateView):
    template_name = 'table/home.html'

    # переменная, в которой удобно хранить данные, записываемые в методах
    # все методы _write_* записывают сюда какие-то данные и потом они возвращаются на клиент
    written_data = {}

    def get_context_data(self, **kwargs):
        context = super(TableView, self).get_context_data()
        # TODO: добавить кэширование
        tables = Table.get_cached_enabled_tables()

        type_table = self.request.GET.get('table', tables.first().name_url)

        limits = Limit.get_cached_enabled_limits_for_table(type_table)

        context['sites'] = Site.get_cached_sites_for_table(type_table)
        context['limits'] = limits
        context['tables'] = tables

        from django.db import connection
        print(len(connection.queries), 'queries')

        return context

    def _get_qs_limits_items(self):
        """Возвращает и кэширует объекты LimitItem, которые добавляются в корзину
        """
        if not getattr(self, 'limit_item_objs', None):
            # сохраняем в кэш
            limit_item_ids = self.request.POST.getlist('limit_items_ids[]')
            limit_item_objs = LimitItem.objects.filter(id__in=limit_item_ids)
            setattr(self, 'limit_item_objs', limit_item_objs)

        return self.limit_item_objs

    def _delete_item_in_cart(self):
        """По id удаляет итем в корзине
        """
        item_id = self.request.POST['item_id']
        # удаляем нужный итем
        del self.request.session['cart_items'][int(item_id)]
        self._write_total_cart()

    def _clear_cart(self):
        try:
            del self.request.session['cart_items']
        except KeyError:
            pass

    def _add_to_cart(self):
        """Добавляет в корзину (по сути в куки) новый объект
        """
        self.written_data = self.request.POST.copy()

        self._write_price()
        self._write_dict_limits_items()

        if 'cart_items' not in self.request.session:
            self.request.session['cart_items'] = [self.written_data]
        else:
            cart_items = self.request.session['cart_items']
            cart_items.append(self.written_data)
            self.request.session['cart_items'] = cart_items

        # обновляем общую сумму корзины
        self._write_total_cart()

    def _write_price(self):
        """Расчитывает цену по входным данным
        """
        self.written_data['price'] = PriceFormation.calculate_order(
            type_package=self.request.POST['type_package'],
            qs_limits_items=self._get_qs_limits_items(),
            term=self.request.POST['term'],
            count_hands=self.request.POST['count_hands'],
            count_tables=self.request.POST['tables']
        )

    def _write_total_cart(self):
        """Расчитывает и записывает тотал в корзину, так же записывает его в self.written_data
        """
        total = PriceFormation.format_00_00(
            sum(float(item['price']) for item in self.request.session['cart_items'])
        )
        self.request.session['total'] = total
        self.written_data['total'] = total

    def _write_dict_limits_items(self):
        result = {}
        for limit_item in self._get_qs_limits_items():
            if not limit_item.site.name in result:
                result[limit_item.site.name] = []

            result[limit_item.site.name].append(limit_item._get_limit().name)

        # преобразуем название лимитов из списка в строку
        for key in result:
            result[key] = ", ".join(result[key])

        self.written_data['limits_item'] = result

    def _write_data_graphics(self):
        """Записывает информацию о статистике лимитов для построения графиков на клиенте
        """
        limit_item_ids = self.request.POST.getlist('limit_items_ids[]')
        if limit_item_ids:
            # теперь переменная нужна как список
            self.written_data = []

            for stat in StatisticLimitItem.objects.filter(limititem__in=limit_item_ids):
                self.written_data.append(
                    {   "limit_id": str(stat.limititem.id),
                        "limit_name": stat.limititem._get_limit().name,
                        "table": stat.limititem._get_limit()._get_table().name,
                        "site": stat.limititem.site.name,
                        "array": StatisticLimitModelForm(instance=stat).as_list_array_count_hands(),
                    }
                )

    def post(self, *args, **kwargs):
        type = self.request.GET['type']

        if type == 'add-to-cart':
            self._add_to_cart()
        elif type == 'delete-item-in-cart':
            self._delete_item_in_cart()
        elif type == 'clear-cart':
            self._clear_cart()
        elif type == 'count-price':
            self._write_price()
        elif type == 'get-data-graphics':
            self._write_data_graphics()

        return HttpResponse(json.dumps(self.written_data))
