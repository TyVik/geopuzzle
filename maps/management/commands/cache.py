import json

from django.core.cache import cache
from django.core.management import BaseCommand, CommandError

from maps.models import Region
from mercator.settings.settings import POLYGON_CACHE_KEY


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('action', metavar='action', help='One of (update/import/export)')
        parser.add_argument('label', metavar='label', help='Cache for action')
        parser.add_argument(
            '--ids', dest='ids', help='Nominates a specific database to load fixtures into. Defaults to the "default" database.',
        )

    def _update(self, query, label, **kwargs):
        for region in query.iterator():
            cache.delete(POLYGON_CACHE_KEY.format(func=label, id=region.id))
            getattr(region, label)

    def _export(self, query, label, **kwargs):
        with open('geocache_{}.json'.format(label), 'w') as f:
            for region in query.iterator():
                result = {region.id: getattr(region, label)}
                f.write(json.dumps(result) + "\n")

    def _import(self, label, **kwargs):
        with open('geocache_{}.json'.format(label), 'r') as f:
            while True:
                region = json.loads(f.readline())
                for rec in region.keys():
                    cache_key = POLYGON_CACHE_KEY.format(func=label, id=rec)
                    cache.set(cache_key, region[rec], timeout=None)

    def handle(self, **options):
        handler = getattr(self, '_{}'.format(options['action']), None)
        if handler is None:
            raise CommandError('Cannot find action')

        if not options['label']:
            raise CommandError('You must specify caches')
        else:
            if options['label'] not in Region.caches():
                raise CommandError('`%s` unknown cache' % options['label'])

        query = Region.objects.all()
        if options['ids']:
            pks = options['ids'].split(',')
            query = query.filter(pk__in=pks)

        handler(query=query, **options)
