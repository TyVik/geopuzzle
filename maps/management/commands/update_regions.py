import json
import os
import shutil
from zipfile import ZipFile

import requests
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core.management import BaseCommand

from django.db import transaction
from hvad.utils import load_translation

from maps.models import Region

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        def import_tree(id):
            def extract_data(properties):
                result = {'level': properties['admin_level']}
                fields = ['boundary', 'ISO3166-1:alpha3', 'timezone']
                for field in fields:
                    result[field] = properties['tags'].get(field, None)
                return result

            def import_region(feature):
                print(feature['properties']['name'])
                parent = None
                if len(feature['rpath']) > 2:
                    # sometimes they are swapped
                    parent_id = feature['rpath'][1] if int(feature['rpath'][0]) == feature['id'] else \
                    feature['rpath'][0]
                    parent = Region.objects.get(osm_id=parent_id)
                region = Region.objects.create(
                    title=feature['properties']['name'],
                    polygon=GEOSGeometry(json.dumps(feature['geometry'])),
                    parent=parent,
                    wikidata_id=feature['properties']['tags'].get('wikidata'),
                    osm_id=feature['id'],
                    osm_data=extract_data(feature['properties'])
                )
                for lang in ('en', 'ru'):
                    trans = load_translation(region, lang, enforce=True)
                    trans.master = region
                    trans.name = region.title
                    trans.save()

            zip_file = os.path.join(settings.GEOJSON_DIR, '{}.zip'.format(id))
            if not os.path.exists(zip_file):
                url = settings.OSM_URL.format(id=id, key=settings.OSM_KEY)
                print(url)
                response = requests.get(url, stream=True)
                if response.status_code != 200:
                    raise Exception('Bad request')
                with open(zip_file, 'wb') as out_file:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, out_file)
            zipfile = ZipFile(zip_file)
            zip_names = zipfile.namelist()
            for zip_name in zip_names:
                print(zip_name)
                if not (zip_name.endswith('AL2.GeoJson') or zip_name.endswith('AL3.GeoJson') or zip_name.endswith('AL4.GeoJson')):
                    continue
                level = json.loads(zipfile.open(zip_name).read().decode())
                not_passed = []
                for feature in level['features']:
                    try:
                        import_region(feature)
                    except Region.DoesNotExist:
                        not_passed.append(feature)
                        continue
                while len(not_passed) > 0:
                    bad_passed = []
                    for feature in not_passed:
                        try:
                            import_region(feature)
                        except Region.DoesNotExist:
                            bad_passed.append(feature)
                            continue
                    if not_passed == bad_passed:
                        print('Circular references')
                        break
                    not_passed = bad_passed

        with open(os.path.join(settings.GEOJSON_DIR, 'root.json')) as root_file:
            root = json.loads(root_file.read())
        for country in root:
            if country['id'] in (1428125, 167454, 51684, 51477, 21335, 62273, 382313, 295480, 60199):
                continue
            print(country['a_attr'])
            if not Region.objects.filter(osm_id=country['id']).exists():
                with transaction.atomic():
                    import_tree(country['id'])
