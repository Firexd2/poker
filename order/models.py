from django.db import models
from django.utils.safestring import mark_safe

from core.tools.mixins.models import NamedObjMixin, OnOffMixin
from table.models import LimitItem


class TypePayment(OnOffMixin, NamedObjMixin):
    """Модель, описывающая вид оплаты
    """
    payment_details = models.TextField('Payment details')

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    type_order = models.CharField('Type order', max_length=12)
    tables = models.TextField('Tables')
    term = models.IntegerField('Term')
    start = models.CharField('Start', max_length=8)
    count = models.TextField('Count')
    limit_items = models.ManyToManyField(LimitItem, verbose_name='Items')
    price = models.FloatField('Price')

    def __str__(self):
        # TODO переделать под render_to_string
        # это __str__ используется для красивого inline отображения итемов в Order
        with open('core/templates/core/inline_order_item.html', 'r') as template:
            template_str = template.read()
            res = template_str.format(self.type_order, self.tables, self.price,
                                      ' <br> '.join([str(limit_item) for limit_item in self.limit_items.all()]))

            if self.type_order == 'Subscription':
                res += '<br> <b>Term</b>: {} <br> <b>Start</b>: {}'.format(self.term, self.start)
            else:
                res += '<br> <b>Count:</b> {}'.format(self.count)

            return mark_safe(res)


class Order(NamedObjMixin):

    email = models.EmailField('E-mail')
    payment = models.ForeignKey(TypePayment, on_delete=models.SET_NULL, null=True, verbose_name='Payment')
    notes = models.TextField('Notes', blank=True, null=True)
    items = models.ManyToManyField(OrderItem, verbose_name='Items')
    total_price = models.FloatField('Total price')

    def __str__(self):
        return self.email
