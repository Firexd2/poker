from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from table.views import TableView

urlpatterns = [
    path('', TableView.as_view()),
    path('contacts/', TemplateView.as_view(template_name='table/contacts.html'))
]
