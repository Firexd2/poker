from django.core.cache import cache


def caching(func):
    """Декоратор, добавляющий кэширование функций, относительно их аргументов
    """

    def wrap(*args):
        cache_name = func.__name__ + ''.join(args)

        result = cache.get(cache_name)
        if not result:
            result = func(*args)
            cache.set(cache_name, result)

        return result

    return wrap


def clearing_cache_decorator(func):
    """Декоратор, который добавляем инвалидацию кэша
    """

    def wrap(self, *args, **kwargs):
        cache.clear()
        return func(self, *args, **kwargs)

    return wrap


def cached_decorator(names_methods):
    """Декоратор моделей, который кэширует методы, указанные в names_funcs
    Для инвалидации кэша декорирует методы save и delete чисткой кэша
    """
    names_methods_for_clearing_cache = 'save', 'delete'

    def wrap(cls):
        # декорируем методы для просчета их кэша
        for name_method in names_methods:
            setattr(cls, name_method, caching(getattr(cls, name_method)))

        # декорируем методы для инвалидации
        for name_method in names_methods_for_clearing_cache:
            setattr(cls, name_method, clearing_cache_decorator(getattr(cls, name_method)))

        return cls

    return wrap
