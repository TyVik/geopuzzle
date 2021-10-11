from __future__ import annotations

import logging

from django import forms
from django.conf import settings
from django.db.models import QuerySet

from common.logging import InMemoryHandler
from .constants import OsmRegionData
from .models import Region, Game
from .wambachers import Wambachers, WambachersNode
from .wikidata import Wikidata

logger = logging.getLogger('commands')


class RegionForm(forms.Form):
    id = forms.ModelMultipleChoiceField(queryset=Region.objects.all(), required=False)
    map = forms.CharField(required=False)

    def __init__(self, game: Game, *args, **kwargs):
        self.game = game
        super().__init__(*args, **kwargs)

    @property
    def regions(self) -> QuerySet[Region]:
        if len(self.cleaned_data['id']) > 0:
            return self.cleaned_data['id']
        return self.game.regions.order_by('?')


class UpdateRegionForm(forms.Form):
    recursive = forms.BooleanField(required=False)
    with_wiki = forms.BooleanField(required=False)
    max_level = forms.IntegerField(initial=8)
    service = Wambachers()

    def _update_geometry(self, item: WambachersNode, with_wiki: bool, max_level: int):
        logger.info('Update geometry for osm_id %s (%s, %s, %s)',
                    item.id, with_wiki, item.children is not None, max_level)
        feature = self.service.load(item)
        defaults = {
            'title': feature.name,
            'polygon': feature.geometry,
            'wikidata_id': feature.wikidata_id,
            'parent': Region.objects.get(osm_id=feature.path[-1]) if feature.path else None,
            'osm_data': OsmRegionData(level=feature.level, boundary=feature.boundary, path=feature.path,
                                      alpha3=feature.alpha3, timezone=feature.timezone)
        }
        region, created = Region.objects.update_or_create(osm_id=feature.osm_id, defaults=defaults)

        if with_wiki and feature.wikidata_id:
            logger.info('Update wiki %s', region.wikidata_id)
            wikidata = Wikidata(region.wikidata_id)
            parent_wiki = None if region.parent is None else region.parent.wikidata_id
            infoboxes = wikidata.get_infoboxes(parent_wiki)
            logger.info('Got wikidata %s', region.wikidata_id)
            for lang in settings.ALLOWED_LANGUAGES:
                trans = region.load_translation(lang)
                trans.infobox = infoboxes[lang]
                trans.save()

        logger.info('Save item %s (new: %s)', region, created)
        if item.children:
            logger.info('Found %s descendants', len(item.children))
            for child in item.children:
                if child.level > max_level:
                    continue
                self._update_geometry(child, with_wiki, max_level)

    def handle(self, region: Region):
        root_logger = logging.getLogger()
        handler = InMemoryHandler(1000, mask='%(name)s:%(lineno)s %(levelname)s %(message)s')
        try:
            root_logger.addHandler(handler)
            item = WambachersNode(id=region.osm_id)
            if self.cleaned_data['recursive']:
                item.children = self.service.fetch_items_list(item)
            self._update_geometry(item, self.cleaned_data['with_wiki'], self.cleaned_data['max_level'])
            return "\n".join(handler.read())
        finally:
            handler.close()
            root_logger.removeHandler(handler)
