from django.db import models

from core.mixins.models.mixins import NamedObjMixin, OnOffMixin


class Site(NamedObjMixin, OnOffMixin):

    # TODO: реализовать remove (удаление итемов)

    class Meta:
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'


class LimitItem(OnOffMixin):

    # TODO: запретить создание и удаление, оставить редактирование

    price = models.IntegerField("Price", default=0)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Site')

    class Meta:
        verbose_name = 'Limit item'
        verbose_name_plural = 'Limit items'


class Limit(NamedObjMixin, OnOffMixin):

    # TODO: реализовать remove (удаление итемов)

    item = models.ManyToManyField(LimitItem, verbose_name='Item', blank=True)

    class Meta:
        verbose_name = 'Limit'
        verbose_name_plural = 'Limits'
