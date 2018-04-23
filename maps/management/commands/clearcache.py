from django.core.cache import cache
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for key in cache.keys('views.decorators.cache*'):
            cache.delete(key)
