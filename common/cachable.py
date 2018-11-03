from django.core.cache import cache

from mercator.settings.settings import POLYGON_CACHE_KEY


def cacheable(func):
    def cache_wrapper(*args, **kwargs):
        self = args[0]
        cache_key = POLYGON_CACHE_KEY.format(func=func.__name__, id=self.id)
        result = cache.get(cache_key)
        if result is None:
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout=None)
        return result
    return cache_wrapper
