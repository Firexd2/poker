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

    price = models.IntegerField("Price", default=0)
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

    # TODO: реализовать remove (удаление итемов)

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
