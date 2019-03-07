import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from table.models import Limit, Site, Table, LimitItem


class TableView(TemplateView):
    template_name = 'table/home.html'

    # переменная, в которой удобно хранить данные, записываемые в методах
    data = {}

    def get_context_data(self, **kwargs):
        context = super(TableView, self).get_context_data()
        # TODO: добавить кэширование
        tables = Table.objects.filter(is_enabled=True)
        type_table = self.request.GET.get('table', tables.first().name_url)

        limits = Limit.objects.filter(is_enabled=True, table__name_url=type_table)

        context['sites'] = Site.objects.filter(limititem__limit__table__name_url=type_table)
        context['limits'] = limits
        context['tables'] = tables
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
        self._count_total_in_cart()

    def _clear_cart(self):
        del self.request.session['cart_items']

    def _count_total_in_cart(self):
        """Расчитывает и записывает тотал в корзину, так же записывает его в self.data
        """
        total = round(sum(item['price'] for item in self.request.session['cart_items']), 2)
        self.request.session['total'] = total
        self.data['total'] = total

    def _add_to_cart(self):
        """Добавляет в корзину (по сути в куки) новый объект
        """
        self.data = self.request.POST.copy()
        self._calculate_order()
        self._fill_dict_limits_items()

        if 'cart_items' not in self.request.session:
            self.request.session['cart_items'] = [self.data]
        else:
            cart_items = self.request.session['cart_items']
            cart_items.append(self.data)
            self.request.session['cart_items'] = cart_items

        # расчитываем общую сумму корзины
        self._count_total_in_cart()

    def _fill_dict_limits_items(self):
        result = {}
        for limit_item in self._get_qs_limits_items():
            if not limit_item.site.name in result:
                result[limit_item.site.name] = []

            result[limit_item.site.name].append(limit_item._get_limit().name)

        # преобразуем название лимитов из списка в строку
        for key in result:
            result[key] = ", ".join(result[key])

        self.data['limits_item'] = result

    def _calculate_order(self):
        """Рассчитывает стоимость выбранных лимитов
        """
        # в базе каждого лимита зафиксирована цена за 1 месяц (30 дней)

        def _calc_additional_price(day):
            """Суть расчета в следующем - есть стартовый добавочный коэффициент, по нему расчитывается добавочная
            стоимость. Если дней больше, чем один - коэффициент будет ниже, и снижаться до 1 он будет до 30 дней (включительно)
            """
            start = 70 * 0.01
            step = start / 29
            return 1 + start - (step * day - step)

        result = 0
        if self.data['type_package'] == 'Subscription':
            # количество дней в заказе
            count_days = int(self.data['term'])
            # количество полных месяцев
            count_full_month = count_days // 30
            # количество месяцев со скидкой
            count_month_with_sale = count_full_month - 1
            # дни, которые не вошли в месяц (к ним должна быть добавлена добавочная розничная стоимость)
            other_days = count_days % 30

            for enum, limit_item in enumerate(self._get_qs_limits_items().order_by('-price_per_month')):
                # промежуточный результат в рамках одного limit_item
                intermediate_result = 0
                # цена за месяц
                price_per_month = limit_item.price_per_month
                # цена за день
                price_per_one_days = price_per_month / 30

                if count_full_month:
                    # первый месяц без скидки, последующие - со скидкой
                    intermediate_result += price_per_month + price_per_month * 0.95 * count_month_with_sale

                if other_days:
                    intermediate_result += price_per_one_days * other_days * _calc_additional_price(other_days)

                # на второй и последуюшие лимиты скидка 50%
                if enum >= 1:
                    intermediate_result *= 0.5

                result += intermediate_result

        else:
            # количество рук
            count_hands = int(self.data['count_hands'].split('K')[0]) / 100  # count 100k
            # количество столов
            count_tables = len(self.data['tables'].split(','))

            for limit_item in self._get_qs_limits_items():
                intermediate_result = 0
                # цена за 100k
                price_per_100k = limit_item.price_per_100k
                # первые 100k рук - без скидки, остальные со скидкой
                intermediate_result += price_per_100k + price_per_100k * (count_hands - 1) * 0.99
                # за каждый стол умножаем цену
                intermediate_result *= count_tables

                result += intermediate_result

        self.data['price'] = round(result, 2)

    def post(self, *args, **kwargs):
        type = self.request.GET['type']

        if type == 'add-to-cart':
            self._add_to_cart()
            return HttpResponse(json.dumps(self.data))
        elif type == 'delete-item-in-cart':
            self._delete_item_in_cart()
            print(self.data)
            return HttpResponse(json.dumps(self.data))
        elif type == 'clear-cart':
            self._clear_cart()
            return HttpResponse(200)
