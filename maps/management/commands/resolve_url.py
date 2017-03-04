import requests
from django.core.management import BaseCommand
from hvad.utils import load_translation

from maps.models import Area

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        def resolve(url):
            response = requests.head(url, allow_redirects=True)
            return response.url

        for area in Area.objects.all():
            for lang in ('en', 'ru'):
                row = load_translation(area, lang, enforce=True)
                if row.infobox is None:
                    print('Empty infobox for area {}, lang {}'.format(area.id, lang))
                    continue
                for attr in ('flag', 'coat_of_arms'):
                    if attr in row.infobox:
                        print(row.infobox[attr])
                        row.infobox[attr] = resolve(row.infobox[attr])
                row.save()
