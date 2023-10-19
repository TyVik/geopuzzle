import logging
from time import sleep
from typing import Dict, Optional

import requests
from django.conf import settings
from django.core.management import BaseCommand
from tqdm import tqdm

from common.constants import LanguageEnumType
from maps.models import Region
from maps.wikidata import Wikidata

logger = logging.getLogger('commands')


def check_link(url, is_image) -> Optional[Dict[LanguageEnumType, dict]]:
    if url:
        response = requests.get(url)
        return (response.status_code != 200) or (is_image and response.headers['content-type'] != 'image/svg+xml')


class Command(BaseCommand):
    CHECKERS = (
        lambda x: check_link(url=x.get('capital', {}).get('wiki'), is_image=False),
        lambda x: check_link(url=x.get('wiki'), is_image=False),
        lambda x: check_link(url=x.get('flag'), is_image=True),
        lambda x: check_link(url=x.get('coat_of_arms'), is_image=True),
    )

    def add_arguments(self, parser):
        parser.add_argument('--since', action='store', type=int, default=None, help='Since id')

    def update_translation(self, area: Region):
        logger.info('Update translation for %s', area)
        wikidata = Wikidata(area.wikidata_id)
        parent_wiki = None if area.parent is None else area.parent.wikidata_id
        infoboxes = wikidata.get_infoboxes(parent_wiki)
        for lang in settings.ALLOWED_LANGUAGES:
            trans = area.load_translation(lang)
            trans.infobox = infoboxes[lang]
            trans.save()

    def should_updated(self, infobox) -> bool:
        for checker in self.CHECKERS:
            if checker(infobox):
                return True
        return False

    def update_region(self, area: Region):
        for lang in settings.ALLOWED_LANGUAGES:
            trans = area.load_translation(lang)
            need_update = self.should_updated(trans.infobox)
            if need_update:
                self.update_translation(area)

    def handle(self, *args, **options):
        query = Region.objects.order_by('id').all()
        if options['since']:
            query = query.filter(pk__gte=options['since'])
        for area in tqdm(query.iterator(), total=query.count()):
            logger.debug('Check region %s', area)
            self.update_region(area)
            sleep(3)
