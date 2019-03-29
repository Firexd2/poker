from django.views.generic import TemplateView

from core.models import Translation, Contact


class BaseView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data()

        context['translation'] = Translation.get_translate_by(self.request.GET.get('lang', ''))
        context['all_translations'] = Translation.objects.all()
        context['contacts'] = Contact.objects.all()
        # переменная, которая хранит строку GET параметра с текущим языком. подставлять на все URL
        context['parameter_lang'] = self._get_parameter_lang()

        return context

    def _get_parameter_lang(self):
        current_lang = self.request.GET.get('lang')
        return 'lang=' + current_lang if current_lang else ''


class OtherPagesView(BaseView):
    page_name = None

    def get_context_data(self, **kwargs):
        context = super(OtherPagesView, self).get_context_data(**kwargs)
        # вытаскиваем и отдаем данные относительно текущего языка
        context['name'] = getattr(context['translation'], self.page_name)
        context['text'] = getattr(context['translation'], 'text_in_' + self.page_name)
        return context
