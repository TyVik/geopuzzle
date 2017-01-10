from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Polygon
from django.core.management import BaseCommand
from django.db import connection

from maps.converter import decode
from maps.models import World

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, available, polygon, answer FROM map_world2")
            rows = cursor.fetchall()
            for row in rows:
                raw = decode(row[2][0][2:-2])
                if raw[0] != raw[-1]:
                    raw.append(raw[0])
                polygons = MultiPolygon(Polygon(raw))
                raw = row[3][1:-1].split(',')
                raw = tuple(map(float, raw))
                answer = Polygon([(raw[0], raw[1]), (raw[2], raw[1]), (raw[2], raw[3]), (raw[0], raw[3]), (raw[0], raw[1])])
                is_available = row[1] if row[1] is not None else False
                World.objects.create(name=row[0], is_available=is_available, polygon=polygons, answer=answer)
