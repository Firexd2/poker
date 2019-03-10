from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Manager

from core.mixins.models.mixins import NamedObjMixin, OnOffMixin, PriorityMixin, DistinctManager
from core.mixins.utils.mixins import name_to_url


class Site(PriorityMixin, NamedObjMixin, OnOffMixin):

    # TODO: реализовать remove (удаление итемов)
    # необходимая мера, так как из особенного ordering (в Meta) появляются дубли
    objects = DistinctManager()

    class Meta:
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'
        ordering = 'limititem__limit__table__priority', 'priority'

    def get_objects_in_view(self):
        """Получаем qs, откуда будем брать объекты для просчета приоритета
        """
        qs = Site.objects.filter(limititem__limit__table=self.__get_table())
        return qs

    def _get_limits_items(self):
        return self.limititem_set.all()

    def __get_table(self):
        """Частный случай получения Table для объектов типа Site
        """
        return self._get_limits_items().first()._get_limit()._get_table()

    def __str__(self):
        try:
            return '{}: {}'.format(self.__get_table().name, self.name)
        except:
            return 'INVALID'


class LimitItem(OnOffMixin):

    price_per_month = models.IntegerField("Price per month", default=0)
    price_per_100k = models.IntegerField("Price per 100k", default=0)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Site')

    class Meta:
        verbose_name = 'Limit item'
        verbose_name_plural = 'Limit items'

    def _get_limit(self):
        return self.limit_set.first()

    def __str__(self):
        # TODO: для отладки
        try:
            return 'Table: {}; Limit: {}; Site: {}'.format(
                self._get_limit()._get_table(),
                self._get_limit().name,
                self.site.name
            )
        except:
            return 'INVALID'


class Limit(PriorityMixin, NamedObjMixin, OnOffMixin):

    items = models.ManyToManyField(LimitItem, verbose_name='Item', blank=True)

    class Meta:
        verbose_name = 'Limit'
        verbose_name_plural = 'Limits'
        ordering = 'table__priority', 'priority'

    def get_objects_in_view(self):
        """Получаем qs, откуда будем брать объекты для просчета приоритета
        """
        return self._get_table().limits

    def _get_table(self):
        """Получаем Table, который ссылается на наш Limit
        """
        return self.table_set.first()

    def __str__(self):

        # TODO: для отладки
        try:
            return '{} ({})'.format(self.name, self._get_table())
        except:
            return 'INVALID'


class Table(PriorityMixin, NamedObjMixin, OnOffMixin):
    limits = models.ManyToManyField('Limit', verbose_name='Limits', blank=True)
    name_url = models.TextField('URL name', blank=True)

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        ordering = 'priority',

    def save(self, *args, **kwargs):
        self.name_url = name_to_url(self.name)
        super(Table, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class PriceFormation(models.Model):
    next_month_discount = models.IntegerField('Next month discount as a percentage', default=5,
                                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    next_limit_discount = models.IntegerField('Next limit discount as a percentage', default=50,
                                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    retail_value_added = models.IntegerField('Retail value added as a percentage', default=70,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    next_100k_hands_discount = models.IntegerField('Next 100k hands discount as a percentage', default=1,
                                                   validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        data = self.next_month_discount, self.next_limit_discount, self.retail_value_added, self.next_100k_hands_discount
        return "Next month discount: {0}%; Next limit discount: {1}%;" \
               " Retail value added: {2}%; Next 100k hands: {3}%".format(*data)

    @classmethod
    def _get_instance(cls):
        return cls.objects.first()

    @staticmethod
    def _clean_data(args):
        """Обработка пришедших с клиента данных для расчетов
        """
        return (
            args['type_package'].lower(), # raw: str
            args['qs_limits_items'], # queryset
            int(args['term']),
            int(args['count_hands'].split('K')[0]) / 100, # raw: '100K hands'
            len(args['count_tables'].split(',')) # raw: 'Heads up, Fullring'
        )

    @classmethod
    def _calc_additional_price(cls, number_day):
        """Суть расчета в следующем - есть стартовый добавочный коэффициент, по нему расчитывается добавочная
        стоимость. Если дней больше, чем один - коэффициент будет ниже, и снижаться до 0 он будет до 30 дней (включительно)
        """
        instance = cls._get_instance()

        retail_value_added_as_dozens = instance.retail_value_added * 0.01
        step_down = retail_value_added_as_dozens / 29

        return 1 + retail_value_added_as_dozens - (step_down * number_day - step_down)

    @staticmethod
    def format_00_00(number):
        """Приводит number к виду 00.00
        """
        str_number = str(round(number, 2))
        if '.' not in str_number:
            return "{}.00".format(str_number)
        else:
            if len(str_number.split('.')[1]) == 2:
                return str_number
            else:
                return str_number + "0"

    @classmethod
    def calculate_order(cls, type_package, qs_limits_items, term, count_hands, count_tables):
        """Рассчитывает стоимость выбранных лимитов
        """
        # обрабатываем сырые данные пришедшие с клиента для дальнейших расчетов
        type_package, qs_limits_items, term, count_hands, count_tables = cls._clean_data(locals())

        # наши настройки формирования цены
        instance = cls._get_instance()

        result = 0

        if type_package == 'subscription':
            # количество полных месяцев
            count_full_month = term // 30
            # количество месяцев со скидкой
            count_month_with_sale = count_full_month - 1
            # дни, которые не вошли в месяц (к ним должна быть добавлена добавочная розничная стоимость)
            other_days = term % 30
            # цена следующего месяца со скидкой в десятках. default: 1 - 5 * 0.01 = 0.95
            next_month_discount_as_dozens = 1 - instance.next_month_discount * 0.01

            # отсортировываем лимиты по схеме: самый дорогой - первый
            for enum, limit_item in enumerate(qs_limits_items.order_by('-price_per_month')):
                # промежуточный результат в рамках одного limit_item
                intermediate_result = 0
                # цена за месяц
                price_per_month = limit_item.price_per_month
                # цена за день
                price_per_one_days = price_per_month / 30

                if count_full_month:
                    # первый месяц без скидки, последующие - со скидкой
                    intermediate_result += price_per_month + price_per_month * next_month_discount_as_dozens * count_month_with_sale

                if other_days:
                    intermediate_result += price_per_one_days * other_days * cls._calc_additional_price(other_days)

                # на второй и последуюшие лимиты скидка
                if enum >= 1:
                    next_limit_discount_as_dozens = instance.next_limit_discount * 0.01
                    intermediate_result *= next_limit_discount_as_dozens

                result += intermediate_result
        else:
            for limit_item in qs_limits_items:
                intermediate_result = 0
                # цена за 100k
                price_per_100k = limit_item.price_per_100k
                next_100k_hands_discount_as_dozens = 1 - instance.next_100k_hands_discount * 0.01
                # первые 100k рук - без скидки, остальные со скидкой
                intermediate_result += price_per_100k + price_per_100k * (count_hands - 1) * next_100k_hands_discount_as_dozens
                # за каждый стол умножаем цену
                intermediate_result *= count_tables

                result += intermediate_result

        return cls.format_00_00(result)
