from django.core.exceptions import ValidationError


def name_to_url(name):
    result = ''
    valid_symbols = "abcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="

    for symbol in name.lower():
        if symbol in valid_symbols:
            result += symbol
    return result


def array_count_validator(value):
    from table.models import StatisticLimitItem
    try:
        values = value.split(',')

        # должно быть _default_count_hands значений
        if len(values) != StatisticLimitItem._default_count_hands:
            raise ValueError()

        # все значения должны быть больше и равно 0
        if any(list(map(lambda x: x < 0, map(int, values)))):
            raise ValueError()
    except:
        if not value.lower() == 'auto':
            raise ValidationError('Please input 30 positive values through separate by comma, or input "auto".')


def make_disabled(modeladmin, request, queryset):
    queryset.update(is_enabled=False)


def make_enabled(modeladmin, request, queryset):
    queryset.update(is_enabled=True)


make_disabled.short_description = "Mark selected as disabled"
make_enabled.short_description = "Mark selected as enabled"
