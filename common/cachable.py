from django.core.cache import cache


def cacheable(func):
    def new_func(*args, **kwargs):
        self = args[0]
        cache_key = self.caches[func.__name__].format(id=self.id)
        result = cache.get(cache_key)
        if result is None:
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout=None)
        return result
    return new_func


class CacheablePropertyMixin(object):
    caches = {}
