import logging

from django.conf import settings
from django.core.management import BaseCommand, CommandError

from maps.constants import OsmRegionData
from maps.models import Region
from maps.wambachers import Wambachers, WambachersNode
from maps.wikidata import Wikidata

logger = logging.getLogger('commands')


MAX_LEVEL = 8


class Command(BaseCommand):
    service = Wambachers()

    def add_arguments(self, parser):
        parser.add_argument('pk', metavar='pk', type=int, help='Region ID')
        parser.add_argument('--recursive', action='store_true', default=False, help='Recursive')
        parser.add_argument('--with-wiki', action='store_true', default=False, help='Update infobox')

    def _update_geometry(self, item: WambachersNode, with_wiki: bool):
        logger.info('Update geometry for osm_id %s', item.id)
        feature = self.service.load(item)
        defaults = {
            'title': feature.name,
            'polygon': feature.geometry,
            'wikidata_id': feature.wikidata_id,
            'parent': Region.objects.get(osm_id=feature.path[0]) if feature.path else None,
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
        if item.children:
            logger.info('Found %s descendants', len(item.children))
            for item in item.children:
                if item.level > MAX_LEVEL:
                    continue
                self._update_geometry(item, with_wiki)

    def handle(self, **options):
        try:
            region = Region.objects.get(pk=options['pk'])
        except ValueError:
            raise CommandError('Please specify the pk')

        item = WambachersNode(id=region.osm_id)
        if options['recursive']:
            item.children = self.service.fetch_items_list(item)
        self._update_geometry(item, options['with_wiki'])
