import difflib
import pprint

import time
from django.core.management import BaseCommand
from hvad.utils import load_translation

from maps.infobox import query_by_wikidata_id
from maps.models import Region

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        for region in Region.objects.filter(wikidata_id__isnull=False, pk__gt=6603).order_by('id').all():
            time.sleep(5)  # protection for DDoS
            wikidata_id = None if region.parent is None else region.parent.wikidata_id
            rows = query_by_wikidata_id(country_id=wikidata_id, item_id=region.wikidata_id)
            for lang, infobox in rows.items():
                trans = load_translation(region, lang, enforce=True)
                print('{} {} ========================================================='.format(region.id, lang))
                diff = ('\n' + '\n'.join(difflib.ndiff(
                    pprint.pformat(trans.infobox).splitlines(),
                    pprint.pformat(infobox).splitlines())))

                print(diff)
                trans.master = region
                trans.infobox = infobox
                trans.name = infobox.get('name', '')
                trans.save()
