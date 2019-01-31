from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html')),
    path('contacts/', TemplateView.as_view(template_name='core/contacts.html'))
]
