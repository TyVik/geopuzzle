import json

from django.contrib.gis.geos import GEOSGeometry
from django.core.management import BaseCommand

from maps.models import Region

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        def import_region(feature):
            def extract_data(properties):
                result = {'level': properties['admin_level']}
                fields = ['boundary', 'ISO3166-1:alpha3', 'timezone']
                for field in fields:
                    result[field] = properties['tags'].get(field, None)
                return result

            print(feature['properties']['name'])
            parent = Region.objects.get(id=7884)
            parent = None
            region = Region.objects.create(
                title=feature['properties']['name'],
                polygon=GEOSGeometry(json.dumps(feature['geometry'])),
                parent=parent,
                wikidata_id=feature['properties']['tags'].get('wikidata'),
                osm_id=feature['id'],
                osm_data=extract_data(feature['properties'])
            )
            for lang in ('en', 'ru'):
                trans = region.load_translation(lang)
                trans.master = region
                trans.name = region.title
                trans.save()
            return region

        with open('Morocco.geojson', 'r') as f:
            geojson = json.loads(f.read())
        for feature in geojson['features']:
            region = import_region(feature)
            print(region.id)
