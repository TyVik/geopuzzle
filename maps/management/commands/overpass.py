import json
import os

from django.contrib.gis.geos import MultiPolygon, GEOSGeometry
from django.core.management import BaseCommand

from maps.models import Region

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


COMMAND = """
relation["boundary"="administrative"]["admin_level"="4"](43648);
(._;>;); out body geom;
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        import overpass
        api = overpass.API()
        response = api.Get(COMMAND, build=False, responseformat='xml')
        with open('tmp.osm', 'w') as f:
            f.write(response)
        os.system('osmtogeojson tmp.osm > tmp.geojson')
        with open('tmp.geojson', 'r') as f:
            geojson = json.loads(f.read())
        region = Region.objects.get(pk=7810)
        polygons = []
        for geom in geojson['features']:
            if geom['geometry']['type'] == 'Polygon':
                polygons.append(GEOSGeometry(json.dumps(geom['geometry'])))
        region.polygon = MultiPolygon(polygons)
        region.save()
        print(response)