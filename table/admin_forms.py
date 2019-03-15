from django import forms

from core.tools.mixins.admin import ModelFormTableMixin
from table.models import Limit, Site, StatisticLimitItem
from datetime import datetime
import random


class StatisticLimitModelForm(forms.ModelForm):

    array_count_hands = forms.CharField(required=True) # TODO: написать валидатор для проверки

    class Meta:
        model = StatisticLimitItem
        exclude = []

    def _get_list_array(self):
        return list(map(int, self.instance.array_count_hands.split(',')))

    def _get_str_array(self, list_array):
        return ', '.join(list(map(str, list_array)))

    def _get_random_value(self):
        """Возвращает рандомное число между min_value и max_value
        """
        return random.randint(self.instance.min_value, self.instance.max_value)

    def as_list_array_count_hands(self):
        """Сериализуем строку array_count_hands в list и отдаем ее. В случае, если необходим просчет нового дня,
        делаем это
        """
        list_array = self._get_list_array()

        now_date = datetime.now().date()

        if now_date != self.instance.date:
            # определяем, сколько дней надо просчитать
            diff = (now_date - self.instance.date).days
            # diff должен быть не больше _default_count_hands
            diff = diff if diff <= StatisticLimitItem._default_count_hands else StatisticLimitItem._default_count_hands

            # добавляем в конец списка новые дни
            for n in list(range(diff)):
                list_array.append(self._get_random_value())

            # удаляем устаревшую инфу
            list_array = list_array[diff:]

            # сохраняем новый список
            self.instance.date = now_date
            self.instance.array_count_hands = self._get_str_array(list_array)
            self.instance.save()

        return list_array


class LimitModelForm(ModelFormTableMixin, forms.ModelForm):

    class Meta:
        model = Limit
        exclude = []


class SiteModelForm(ModelFormTableMixin, forms.ModelForm):

    class Meta:
        model = Site
        exclude = []
