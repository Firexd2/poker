from django.db import models

from core.tools.mixins.models import NamedObjMixin, OnOffMixin
from table.models import LimitItem


class TypePayment(OnOffMixin, NamedObjMixin):
    """Модель, описывающая вид оплаты
    """
    payment_details = models.TextField('Payment details')
    description = models.TextField('Description')

    def __str__(self):
        return self.name


class Order(NamedObjMixin):

    email = models.EmailField('E-mail')
    payment = models.ForeignKey(TypePayment, on_delete=models.SET_NULL, null=True, verbose_name='Payment')
    limit_items = models.ManyToManyField(LimitItem, verbose_name='Items')
    notes = models.TextField('Notes', blank=True, null=True)
