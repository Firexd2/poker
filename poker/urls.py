from django.urls import path
from django.views.generic import TemplateView

from table.admin import admin_site
from table.views import TableView

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', TableView.as_view()),
    #path('order/', ),
    path('contacts/', TemplateView.as_view(template_name='order/order.html'))
]
