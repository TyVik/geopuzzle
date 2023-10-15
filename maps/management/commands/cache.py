import json

from django.core.cache import cache
from django.core.management import BaseCommand
from tqdm import tqdm

from maps.models import Region
from mercator.settings.settings import POLYGON_CACHE_KEY


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('action', metavar='action', choices=["update", "import", "export"])
        parser.add_argument('label', metavar='label', choices=[cache for cache in Region.caches()])
        parser.add_argument('--ids', dest='ids', help='Objects pk in database')

    def _update(self, query, label, **kwargs):
        for region in tqdm(query.iterator(), total=query.count()):
            cache.delete(POLYGON_CACHE_KEY.format(func=label, id=region.pk))
            getattr(region, label)

    def _export(self, query, label, **kwargs):
        with open('geocache_{}.json'.format(label), 'w') as f:
            for region in tqdm(query.iterator(), total=query.count()):
                result = {region.pk: getattr(region, label)}
                f.write(json.dumps(result) + "\n")

    def _import(self, label, **kwargs):
        with open('geocache_{}.json'.format(label), 'r') as f:
            while region := json.loads(f.readline()):
                for rec in region.keys():
                    cache_key = POLYGON_CACHE_KEY.format(func=label, id=rec)
                    cache.set(cache_key, region[rec], timeout=None)

    def handle(self, **options):
        handler = getattr(self, '_{}'.format(options['action']), None)
        query = Region.objects.all()
        if options['ids']:
            pks = options['ids'].split(',')
            query = query.filter(pk__in=pks)

        handler(query=query, **options)
