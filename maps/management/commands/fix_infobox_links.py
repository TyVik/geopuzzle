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


def fix(area: Region, lang: str, text: str) -> Optional[Dict[LanguageEnumType, dict]]:
    logger.info('Fix %s with language %s: %s', area, lang, text)
    wikidata = Wikidata(area.wikidata_id)
    parent_wiki = None if area.parent is None else area.parent.wikidata_id
    return wikidata.get_infoboxes(parent_wiki)


def check_link(area, lang, infobox, name, is_image) -> Optional[Dict[LanguageEnumType, dict]]:
    url = infobox[name]
    if url:
        response = requests.get(url)
        if response.status_code != 200:
            return fix(area, lang, '- {} link'.format(name))
        if is_image and response.headers['content-type'] != 'image/svg+xml':
            return fix(area, lang, '- {} svg'.format(name))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--since', action='store', type=int, default=None, help='Since id')

    def handle(self, *args, **options):
        query = Region.objects.order_by('id').all()
        if options['since']:
            query = query.filter(pk__gte=options['since'])
        for area in tqdm(query.iterator(), total=query.count()):
            logger.debug('Check region %s', area)
            updated = None
            for lang in settings.ALLOWED_LANGUAGES:
                trans = area.load_translation(lang)
                infobox = trans.infobox
                if 'capital' in infobox and isinstance(infobox['capital'], dict) and 'wiki' in infobox['capital']:
                    updated = check_link(area, lang, infobox['capital'], 'wiki', False)

                if 'wiki' in infobox and updated is None:
                    updated = check_link(area, lang, infobox, 'wiki', False)
                if 'flag' in infobox and updated is None:
                    updated = check_link(area, lang, infobox, 'flag', True)
                if 'coat_of_arms' in infobox and updated is None:
                    updated = check_link(area, lang, infobox, 'coat_of_arms', True)

            if updated:
                logger.info('Update translation for %s', area)
                for lang in settings.ALLOWED_LANGUAGES:
                    trans = area.load_translation(lang)
                    trans.infobox = updated[lang]
                    trans.save()
            sleep(3)
