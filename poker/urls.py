from django.urls import path

from core.views import OtherPagesView
from order.views import OrderView
from table.admin import admin_site
from table.views import TableView

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', TableView.as_view()),
    path('order/', OrderView.as_view()),
    path('about/', OtherPagesView.as_view(page_name='about', template_name='core/other_pages.html')),
    path('sales/', OtherPagesView.as_view(page_name='sales', template_name='core/other_pages.html')),
    path('articles/', OtherPagesView.as_view(page_name='articles', template_name='core/other_pages.html')),
    path('faq/', OtherPagesView.as_view(page_name='faq', template_name='core/other_pages.html')),
]
