from django import template

register = template.Library()


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)


@register.filter
def is_enabled_site(queryset):
    return queryset.filter(site__is_enabled=True)
