import requests
from django.conf import settings
from django.core.management import BaseCommand

from maps.models import Region


def log(area: Region, lang: str, text: str):
    print('Region {} with language {}: {}'.format(area.id, lang, text))


def check_link(area, lang, infobox, name, is_image):
    response = requests.get(infobox[name])
    if response.status_code != 200:
        log(area, lang, '- {} link'.format(name))
    if is_image and response.headers['content-type'] != 'image/svg+xml':
        log(area, lang, '- {} svg'.format(name))


class Command(BaseCommand):
    def handle(self, *args, **options):
        for area in Region.objects.order_by('id').all():
            for lang in settings.ALLOWED_LANGUAGES:
                trans = area.load_translation(lang)
                infobox = trans.infobox
                if 'area' not in infobox:
                    log(area, lang, '- area')
                if 'population' not in infobox:
                    log(area, lang, '- population')
                if 'name' not in infobox:
                    log(area, lang, '- name')
                if 'geonamesID' not in infobox:
                    log(area, lang, '- geonamesID')
                if 'currency' not in infobox and area.country.is_global:
                    log(area, lang, '- currency')

                if 'capital' not in infobox or not isinstance(infobox['capital'], dict):
                    log(area, lang, '- capital')
                else:
                    if not isinstance(infobox['capital']['lat'], float):
                        log(area, lang, '- capital/lat')
                    if not isinstance(infobox['capital']['lon'], float):
                        log(area, lang, '- capital/lon')
                    if 'wiki' not in infobox['capital']:
                        log(area, lang, '- capital/wiki')
                    else:
                        check_link(area, lang, infobox['capital'], 'wiki', False)

                if 'wiki' not in infobox:
                    log(area, lang, '- wiki')
                else:
                    check_link(area, lang, infobox, 'wiki', False)
                if 'flag' not in infobox:
                    log(area, lang, '- flag')
                else:
                    check_link(area, lang, infobox, 'flag', True)
                if 'coat_of_arms' not in infobox:
                    log(area, lang, '- coat_of_arms')
                else:
                    check_link(area, lang, infobox, 'coat_of_arms', True)