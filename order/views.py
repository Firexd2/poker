from django.views.generic import FormView

from core.views import BaseView
from order.forms import OrderForm
from table.views import TableView


class OrderView(FormView, BaseView):

    form_class = OrderForm
    template_name = 'order/order.html'
    success_url = '/?status=success'

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.save()

        # добавляем из корзины итемы
        new_obj.limit_items.add(*self.request.session['ids'])
        # подчищаем сессию
        TableView.clear_cart(self)
        # TODO отправление e-mail пользователю и админу

        return super(OrderView, self).form_valid(form)
