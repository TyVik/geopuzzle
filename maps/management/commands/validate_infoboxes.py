import requests
from django.conf import settings
from django.core.management import BaseCommand

from maps.models import Region


def log(area, lang, text):
    print(f'Region {area.id} with language {lang}: {text}')


def check_link(area, lang, infobox, name, is_image):
    response = requests.get(infobox[name])
    if response.status_code != 200:
        log(area, lang, f'- {name} link')
    if is_image and response.headers['content-type'] != 'image/svg+xml':
        log(area, lang, f'- {name} svg')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for area in Region.objects.order_by('id').all():
            for lang in settings.LANGUAGES:
                trans = area.load_translation(lang[0])
                infobox = trans.infobox
                if 'area' not in infobox:
                    log(area, lang[0], '- area')
                if 'population' not in infobox:
                    log(area, lang[0], '- population')
                if 'name' not in infobox:
                    log(area, lang[0], '- name')
                if 'geonamesID' not in infobox:
                    log(area, lang[0], '- geonamesID')
                if 'currency' not in infobox and area.country.is_global:
                    log(area, lang[0], '- currency')

                if 'capital' not in infobox or not isinstance(infobox['capital'], dict):
                    log(area, lang[0], '- capital')
                else:
                    if not isinstance(infobox['capital']['lat'], float):
                        log(area, lang[0], '- capital/lat')
                    if not isinstance(infobox['capital']['lon'], float):
                        log(area, lang[0], '- capital/lon')
                    if 'wiki' not in infobox['capital']:
                        log(area, lang[0], '- capital/wiki')
                    else:
                        check_link(area, lang[0], infobox['capital'], 'wiki', False)

                if 'wiki' not in infobox:
                    log(area, lang[0], '- wiki')
                else:
                    check_link(area, lang[0], infobox, 'wiki', False)
                if 'flag' not in infobox:
                    log(area, lang[0], '- flag')
                else:
                    check_link(area, lang[0], infobox, 'flag', True)
                if 'coat_of_arms' not in infobox:
                    log(area, lang[0], '- coat_of_arms')
                else:
                    check_link(area, lang[0], infobox, 'coat_of_arms', True)