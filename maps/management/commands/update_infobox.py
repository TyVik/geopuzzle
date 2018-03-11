import difflib
import pprint

import time
from django.core.management import BaseCommand

from maps.infobox import query_by_wikidata_id
from maps.models import Region


class Command(BaseCommand):
    def handle(self, *args, **options):
        for region in Region.objects.filter(wikidata_id__isnull=False, pk__gt=6603).order_by('id').all():
            time.sleep(5)  # protection for DDoS
            wikidata_id = None if region.parent is None else region.parent.wikidata_id
            rows = query_by_wikidata_id(country_id=wikidata_id, item_id=region.wikidata_id)
            for lang, infobox in rows.items():
                trans = region.load_translation(lang)
                print(f'{region.id} {lang} =========================================================')
                diff = ('\n' + '\n'.join(difflib.ndiff(
                    pprint.pformat(trans.infobox).splitlines(),
                    pprint.pformat(infobox).splitlines())))

                print(diff)
                trans.master = region
                trans.infobox = infobox
                trans.name = infobox.get('name', '')
                trans.save()
