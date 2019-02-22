from django.views.generic import TemplateView

from table.models import Limit, Site, Table


class TableView(TemplateView):
    template_name = 'table/home.html'

    def get_context_data(self, **kwargs):
        context = super(TableView, self).get_context_data()

        tables = Table.objects.filter(is_enabled=True)
        type_table = self.request.GET.get('table', tables.first().name_url)

        limits = Limit.objects.filter(is_enabled=True, table__name_url=type_table).order_by('name')

        context['sites'] = Site.objects.filter(limititem__limit__table__name_url=type_table).distinct().order_by('name')
        context['limits'] = limits
        context['tables'] = tables
        return context
