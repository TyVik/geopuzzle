import json
import sys

from django.core.cache import cache
from django.core.management.base import LabelCommand, CommandError

from maps.models import Region

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(LabelCommand):
    def handle(self, *labels, **options):
        if not labels:
            print(self.print_help('import_cache', ''))
            sys.exit(1)

        for label in labels:
            if label not in Region.caches.keys():
                raise CommandError('`%s` unknown cache' % label)
            with open('geocache_{}.json'.format(label), 'r') as f:
                while True:
                    region = json.loads(f.readline())
                    for rec in region.keys():
                        cache_key = Region.caches[label].format(id=rec)
                        cache.set(cache_key, region[rec], timeout=None)
