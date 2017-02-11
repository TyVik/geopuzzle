from django.core.management import BaseCommand
from django.db import connection

__authors__ = "Viktor Tyshchenko"
__copyright__ = "Copyright (C) 3D4Medical.com, LLC - All Rights Reserved"
__license__ = "Unauthorized copying of this file, via any medium is strictly prohibited. Proprietary and confidential"


IDS = (208, 183, 174, 110, 106, 69, 48)
COUNTRY_ID = 9
COPY_SQL = 'INSERT INTO maps_area(difficulty, polygon, answer, country_id) SELECT 2, polygon, answer, {country_id} from maps_area where id = {id} returning ID'
COPY_SQL_TRANS = 'INSERT INTO maps_area_translation(name, infobox, language_code, master_id) SELECT name, infobox, language_code, {new_id} from maps_area_translation where master_id = {id}'


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            for id in IDS:
                cursor.execute(COPY_SQL.format(country_id=COUNTRY_ID, id=id))
                row = cursor.fetchone()
                new_id = row[0]
                cursor.execute(COPY_SQL_TRANS.format(new_id=new_id, id=id))
