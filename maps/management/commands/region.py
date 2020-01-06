import logging

from django.conf import settings
from django.core.management import BaseCommand, CommandError

from maps.constants import OsmRegionData
from maps.models import Region
from maps.wambachers import Wambachers
from maps.wikidata import Wikidata

logger = logging.getLogger('commands')


MAX_LEVEL = 8


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('action', metavar='action', help='One of (update)')
        parser.add_argument('pk', metavar='pk', type=int, help='Region ID')
        parser.add_argument('--recursive', action='store_true', default=False, help='Recursive')
        parser.add_argument('--with-wiki', action='store_true', default=False, help='Update infobox')

    def _update(self, osm_id: int, level: int, recursive: bool, with_wiki: bool):
        logger.info('Start process item: osm_id %s, level %s', osm_id, level)
        service = Wambachers(osm_id)
        service.load(level)
        feature = service.features[0]
        defaults = {
            'title': feature.name,
            'polygon': feature.geometry,
            'wikidata_id': feature.wikidata_id,
            'parent': Region.objects.get(osm_id=feature.path[1]) if feature.path[1] != 0 else None,
            'osm_data': OsmRegionData(level=feature.level, boundary=feature.boundary, path=feature.path,
                                      alpha3=feature.alpha3, timezone=feature.timezone)
        }
        region, created = Region.objects.update_or_create(osm_id=feature.osm_id, defaults=defaults)

        if with_wiki and feature.wikidata_id:
            wikidata = Wikidata(region.wikidata_id)
            parent_wiki = None if region.parent is None else region.parent.wikidata_id
            infoboxes = wikidata.get_infoboxes(parent_wiki)
            for lang in settings.ALLOWED_LANGUAGES:
                trans = region.load_translation(lang)
                trans.infobox = infoboxes[lang]
                trans.save()

        logger.info('Save item %s (new: %s)', region, created)
        if recursive:
            items = service.fetch_items_list()
            logger.info('Found %s descendants', len(items))
            for item in items:
                if item.level > MAX_LEVEL:
                    continue
                self._update(item.id, item.level, recursive, with_wiki)

    def handle(self, **options):
        handler = getattr(self, '_{}'.format(options['action']), None)
        if handler is None:
            raise CommandError('Cannot find action')

        try:
            region = Region.objects.get(pk=options['pk'])
        except ValueError:
            raise CommandError('Please. specify the pk')

        handler(region.osm_id, region.osm_data['level'], options['recursive'], options['with_wiki'])
