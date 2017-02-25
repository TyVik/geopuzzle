from django.core.management import BaseCommand
from hvad.utils import load_translation

from maps.models import Area

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        for area in Area.objects.filter(wikidata_id__isnull=True).all():
            translataion = load_translation(area, 'en', enforce=False)
            if translataion.infobox is None:
                print(area.id)
                continue
            instance = translataion.infobox.get('instance', None)
            if instance is None:
                print(area.id)
            else:
                area.wikidata_id = instance.split('/')[-1]
                area.save()
