from django.contrib.gis.geos import MultiPolygon
from django.core.management import BaseCommand

from maps.models import Region


class InconsistItems(Exception):
    pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        def check_region(region: Region):
            osm_items = region.fetch_items_list()
            osm_list = [(osm['id'], osm['data']['admin_level']) for osm in osm_items if osm['data']['admin_level'] < 8]
            my_list = [(child.osm_id, child.osm_data['level']) for child in region.region_set.all()]

            try:
                if len(osm_list) != len(my_list):
                    raise InconsistItems(f'{region.id}: {osm_list} != {my_list}')
                for item in my_list:
                    if item not in osm_list:
                        raise InconsistItems(f'{region.id}: {osm_list} != {my_list}')
            except InconsistItems:
                region.region_set.update(is_enabled=False, parent=None)
                for item in osm_items:
                    if item['data']['admin_level'] >= 8:
                        continue
                    defaults = {
                        'parent': region,
                        'osm_data': {'level': item['data']['admin_level']},
                        'polygon': MultiPolygon(),
                    }
                    child, created = Region.objects.get_or_create(osm_id=item['id'], defaults=defaults)
                    if created:
                        child.fetch_polygon()
                        child.fetch_infobox()
                    else:
                        child.parent = region
                        child.is_enabled = True
                        child.save()
            region.refresh_from_db()
            for item in region.region_set.all():
                check_region(item)

        for country in Region.objects.filter(id=1206).order_by('id').iterator():
            check_region(country)
