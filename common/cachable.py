from typing import Callable, Any

from django.core.cache import cache

from mercator.settings.settings import POLYGON_CACHE_KEY


def cacheable(ttl=None):
    def inner_cacheable(func: Callable) -> Callable:
        def cache_wrapper(*args, **kwargs) -> Any:
            self = args[0]
            pk = self if isinstance(self, str) else self.pk
            cache_key = POLYGON_CACHE_KEY.format(func=func.__name__, id=pk)
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout=ttl)
            return result
        return cache_wrapper

    return inner_cacheable
