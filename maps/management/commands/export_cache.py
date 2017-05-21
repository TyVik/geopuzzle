import json
import sys
from django.core.management.base import LabelCommand, CommandError

from maps.models import Region

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(LabelCommand):
    def handle(self, *labels, **options):
        if not labels:
            print(self.print_help('export_cache', ''))
            sys.exit(1)

        for label in labels:
            if label not in Region.caches.keys():
                raise CommandError('`%s` unknown cache' % label)
            with open('geocache_{}.json'.format(label), 'w') as f:
                for region in Region.objects.all().iterator():
                    result = {region.id: getattr(region, label)}
                    f.write(json.dumps(result) + "\n")
