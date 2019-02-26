from django.db import models

from core.mixins.models.mixins import NamedObjMixin, OnOffMixin
from core.mixins.utils.mixins import name_to_url


class Site(NamedObjMixin, OnOffMixin):

    # TODO: реализовать remove (удаление итемов)

    class Meta:
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.limititem_set.all().first().limit_set.all().first().table_set.all().first().name)
        except:
            return 'INVALID'


class LimitItem(OnOffMixin):

    price = models.IntegerField("Price", default=0)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Site')

    class Meta:
        verbose_name = 'Limit item'
        verbose_name_plural = 'Limit items'

    def __str__(self):
        limit = self.limit_set.all().first()
        # TODO: для отладки
        try:
            return 'Table: {}; Limit: {}; Site: {}'.format(limit.table_set.all().first().name, limit.name, self.site.name)
        except:
            return 'INVALID'


class Limit(NamedObjMixin, OnOffMixin):

    # TODO: реализовать remove (удаление итемов)

    item = models.ManyToManyField(LimitItem, verbose_name='Item', blank=True)

    class Meta:
        verbose_name = 'Limit'
        verbose_name_plural = 'Limits'

    def __str__(self):

        # TODO: для отладки
        try:
            return '{} ({})'.format(self.name, self.table_set.all().first().name)
        except:
            return 'INVALID'


class Table(NamedObjMixin, OnOffMixin):
    limit = models.ManyToManyField('Limit', verbose_name='Limits', blank=True)
    name_url = models.TextField('URL name', blank=True)

    # TODO: запретить создавать новые столы

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"

    def save(self, *args, **kwargs):
        self.name_url = name_to_url(self.name)
        super(Table, self).save(*args, **kwargs)
