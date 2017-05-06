from django.core.management import BaseCommand
from django.core.files.storage import default_storage

from cairosvg.surface import PNGSurface

from maps.models import Region

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        for lang in ('en', 'ru'):
            for area in Region.objects.language(lang).all():
                infobox = area.infobox

                for key in ('s', 'label'):
                    if key in infobox:
                        del(infobox[key])

                if 'area' in infobox:
                    infobox['area'] = str(int(float(infobox['area'])))

                png_name = 'flags/' + infobox['flag'].split('/')[-1].replace('svg', 'png')
                png_path = default_storage.path(png_name)
                PNGSurface.convert(url=infobox['flag'], write_to=png_path)
                infobox['flag'] = default_storage.url(png_name)

                area.infobox = infobox
                area.save()
