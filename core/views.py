from django.views.generic import TemplateView

from core.models import Translation, Contact


class BaseView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data()
        lang = self.request.GET.get('lang', 'EN')
        context['translation'] = Translation.get_translate_by(lang)
        context['contacts'] = Contact.objects.all()

        return context


class OtherPagesView(BaseView):
    page_name = None

    def get_context_data(self, **kwargs):
        context = super(OtherPagesView, self).get_context_data(**kwargs)
        # вытаскиваем и отдаем данные относительно текущего языка
        context['name'] = getattr(context['translation'], self.page_name)
        context['text'] = getattr(context['translation'], 'text_in_' + self.page_name)
        return context
