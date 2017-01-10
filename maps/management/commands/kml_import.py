from django.db import connection
from lxml import etree as ET

from django.core.management import BaseCommand

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            tree = ET.parse('World.kml')
            placemarks = tree.xpath('//kml:Placemark', namespaces={'kml': "http://www.opengis.net/kml/2.2"})
            for placemark in placemarks:
                name = placemark.xpath('./kml:name/text()', namespaces={'kml': "http://www.opengis.net/kml/2.2"})[0]
                geometry = placemark.xpath('./kml:MultiGeometry', namespaces={'kml': "http://www.opengis.net/kml/2.2"})[0]
                multipolygon = ''
                many = 0
                for polygon in geometry.xpath('./kml:Polygon', namespaces={'kml': "http://www.opengis.net/kml/2.2"}):
                    multipolygon += ET.tostring(polygon).decode('utf-8')
                    many += 1
                if many > 1:
                    print('<MultiGeometry>{}</MultiGeometry>'.format(multipolygon))
                    cursor.execute(
                        "insert into maps_world(name, is_available, polygon) values(%s, %s, ST_GeomFromKml(%s::text))",
                        [name, True, '<MultiGeometry>{}</MultiGeometry>'.format(multipolygon)])
                else:
                    cursor.execute(
                        "insert into maps_world(name, is_available, polygon) values(%s, %s, ST_Multi(ST_GeomFromKml(%s::text)))",
                        [name, True, multipolygon])
                print('---------')
