from django.shortcuts import render
from django.views.generic import TemplateView

from table.models import Limit, Site


class TableView(TemplateView):
    template_name = 'table/home.html'

    def get_context_data(self, **kwargs):
        context = super(TableView, self).get_context_data()
        context['sites'] = Site.objects.all().order_by('name')
        context['limits'] = Limit.objects.all()
        return context
