import re


def name_to_url(name):
    result = ''
    valid_symbols = "abcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="

    for symbol in name.lower():
        if symbol in valid_symbols:
            result += symbol
    return result


def make_disabled(modeladmin, request, queryset):
    queryset.update(is_enabled=False)


def make_enabled(modeladmin, request, queryset):
    queryset.update(is_enabled=True)


make_disabled.short_description = "Mark selected as disabled"
make_enabled.short_description = "Mark selected as enabled"
