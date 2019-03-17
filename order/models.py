from django.db import models

from core.tools.mixins.models import NamedObjMixin
from table.models import LimitItem


class TypePayment(NamedObjMixin):
    """Модель, описывающая вид оплаты
    """
    requisite = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):

    email = models.EmailField()
    payment = models.ForeignKey(TypePayment, on_delete=models.SET_NULL, null=True)
    limit_items = models.ManyToManyField(LimitItem)
    notes = models.TextField(blank=True, null=True)
