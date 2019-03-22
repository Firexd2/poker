from django.views.generic import TemplateView


class OtherPagesView(TemplateView):
    page_name = None

    def get_context_data(self, **kwargs):
        context = super(OtherPagesView, self).get_context_data(**kwargs)
        context['page_name'] = self.page_name
        return context
