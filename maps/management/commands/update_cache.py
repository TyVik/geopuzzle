from django.core.management import BaseCommand

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
                for cache_name in area.caches:
                    getattr(area, cache_name)()
