import difflib
import pprint

import time
from django.core.management import BaseCommand
from hvad.utils import load_translation

from maps.infobox import query_by_wikidata_id
from maps.models import Area

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        for area in Area.objects.filter(wikidata_id__isnull=False).order_by('id').all():
            time.sleep(5)  # protection for DDoS
            wikidata_id = None if area.country.is_global else area.country.wikidata_id
            rows = query_by_wikidata_id(country_id=wikidata_id, item_id=area.wikidata_id)
            for lang, infobox in rows.items():
                trans = load_translation(area, lang, enforce=True)
                print('{} {} ========================================================='.format(area.id, lang))
                diff = ('\n' + '\n'.join(difflib.ndiff(
                    pprint.pformat(trans.infobox).splitlines(),
                    pprint.pformat(infobox).splitlines())))

                print(diff)
                trans.master = area
                trans.infobox = infobox
                trans.name = infobox.get('name', '')
                trans.save()
