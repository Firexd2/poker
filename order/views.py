from django.views.generic import FormView

from core.models import EmailBackendSetting, Translation
from core.views import BaseView
from order.forms import OrderForm
from order.models import OrderItem
from table.views import TableView


class OrderView(FormView, BaseView):
    form_class = OrderForm
    template_name = 'order/order.html'
    success_url = '/?status=success'

    def get_success_url(self):
        res = self.success_url
        if self._get_parameter_lang():
            res += '&' + self._get_parameter_lang()
        return res

    def form_valid(self, form):
        new_order = form.save(commit=False)

        order_items = set()

        for cart_item in self.request.session['cart_items']:
            order_item = OrderItem.objects.create(
                type_order=cart_item['type_package'],
                tables=cart_item['tables'],
                term=cart_item.get('term', ''),
                count=cart_item.get('count_hands'),
                start=cart_item.get('start_date', ''),
                price=cart_item['price']
            )
            order_item.limit_items.add(*cart_item['limit_items_ids[]'])
            order_items.add(order_item)

        # добавляем из корзины итемы
        new_order.total_price = self.request.session['total']
        new_order.save()
        new_order.items.add(*order_items)

        # подчищаем сессию
        TableView.clear_cart(self)
        # TODO отправление e-mail пользователю и админу

        translation = Translation.get_translation_by(self.request.GET.get('lang', ''))

        # TODO: прикрутить сюда Celery
        # отправляем пользователю письмо о заказе
        EmailBackendSetting.send_email(
            subject=translation.email_letter_subject_for_client,
            body=translation.email_letter_body_for_client.format(client_name=new_order.name,
                                                                 type_payment=new_order.payment.name,
                                                                 details_payment=new_order.payment.payment_details,
                                                                 total_price=new_order.total_price,
                                                                 items='<br> '.join(
                                                                     [str(i) for i in new_order.items.all()])),
            to=new_order.email
        )
        # отправляем админу письмо о заказе
        EmailBackendSetting.send_email(
            subject=translation.email_letter_subject_for_admin,
            body=translation.email_letter_body_for_admin.format(client_name=new_order.name,
                                                                type_payment=new_order.payment.name,
                                                                details_payment=new_order.payment.payment_details,
                                                                total_price=new_order.total_price,
                                                                items='<br> '.join(
                                                                    [str(i) for i in new_order.items.all()]),
                                                                notes=new_order.notes),
        )

        return super(OrderView, self).form_valid(form)
