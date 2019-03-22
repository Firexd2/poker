# TODO: таблица переводов
# TODO: добавить динамичесоке отображдение преимуществ
from django.db import models

from core.tools.mixins.models import NamedObjMixin, OnOffMixin, PriorityMixin


class Contact(PriorityMixin, NamedObjMixin):
    contact = models.TextField() # TODO: переименовать в text

    # TODO добавить в админку

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = 'priority',

    def __str__(self):
        return self.name


class Translations(OnOffMixin, PriorityMixin, NamedObjMixin):
    """Таблица, в которой хранятся все переводы
    Под name хранится название языка
    """
    # TODO: imagefield для флага


    site_name = models.CharField("Site name", max_length=18)

    # данные для таблицы
    subscription = models.TextField("Subscription", default="Subscription") # TODO: перевод для корзины
    limits = models.TextField("Limits", default="Limits")
    package = models.TextField("Package", default="Package")
    tables_sizes = models.TextField("Tables sizes", default="Tables sizes")
    start_subscription = models.TextField("Start subscription", default="Start subscription")
    term = models.TextField("Term", default="Term")
    numbers_of_hands = models.TextField("Numbers of hands", default="Numbers of hands")
    next_limit = models.TextField("Next limit", default="next limit")
    next_month = models.TextField("Next month", default="next month")
    next_100k = models.TextField("Next 100k", default="next 100k")
    cart_content = models.TextField("Cart content", default="Cart content")
    clear = models.TextField("Clear", default="clear")
    days_from = models.TextField("Days from", default="days from")
    price = models.TextField("Price", default="Price")
    total = models.TextField("Total", default="Total")
    make_order = models.TextField("Make order", default="Make order")
    add_to_cart = models.TextField("Add to cart", default="Add to cart")
    order = models.TextField("Order", default="Order")
    game = models.TextField("Game", default="Game")
    limits = models.TextField("Limits", default="Limits")
    tables = models.TextField("Tables", default="Tables")
    start = models.TextField("Start", default="Start")
    past = models.TextField("Past", default="past")