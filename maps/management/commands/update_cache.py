from django.core.cache import cache
from django.core.management import BaseCommand

from maps.converter import encode_coords

from maps.models import Country

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Update cache:')
        for country in Country.objects.language('en').all():
            print(' - {}'.format(country.name))
            for area in country.area_set.all():
                for cache_name, cache_template in area.caches.items():
                    cache_key = cache_template.format(id=area.id)
                    if cache_name == 'polygon_gmap':
                        result = []
                        for polygon in area.polygon:
                            result.append(encode_coords(polygon.coords[0]))
                            if len(polygon.coords) > 1:
                                result.append(encode_coords(polygon.coords[1]))
                        cache.set(cache_key, result, timeout=None)
