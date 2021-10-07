import gzip
import json
import logging
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional

import requests
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon

logger = logging.getLogger('wambachers')


@dataclass
class WambachersNode:
    id: int
    text: Optional[str] = None
    level: Optional[int] = None
    children: List['WambachersNode'] = None

    @property
    def osm_id(self) -> int:
        return -1 * self.id

    @property
    def geojson_path(self) -> Path:
        return settings.GEOJSON_DIR.joinpath(f'{self.id}.geojson')

    @property
    def boundaries_url(self) -> str:
        return settings.OSM_URL.format(id=self.osm_id, key=settings.OSM_KEY)


@dataclass
class Feature:  # pylint: disable=too-many-instance-attributes
    geometry: GEOSGeometry
    osm_id: int
    wikidata_id: str
    level: int
    boundary: str
    name: str
    path: List[int]
    alpha3: str
    timezone: str
    lang: Dict[str, str]


class Wambachers:
    def fetch_items_list(self, item: WambachersNode) -> List[WambachersNode]:
        def parse(items: List) -> List[WambachersNode]:
            return [WambachersNode(
                id=abs(item['id']),
                text=item['name'],
                level=item['admin_level'],
                children=parse(item['children']))
                    for item in items if item['boundary'] == 'administrative']

        def find_subtree(tree: List[WambachersNode], item: WambachersNode) -> Optional[WambachersNode]:
            for child in tree:
                if child.id == item.id:
                    return child
                in_tree = find_subtree(child.children, item)
                if in_tree:
                    return in_tree
            return None

        feature = self.load(item)
        root = WambachersNode(feature.path[-1]) if feature.path else item
        params = {'db': 'osm20210531', 'rootId': root.osm_id}
        headers = {
            'Referer': 'https://osm-boundaries.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        response = requests.post('https://osm-boundaries.com/Ajax/GetTreeContent',
                                 params=params, headers=headers)
        tree = parse(response.json())
        subtree = find_subtree(tree, item)
        return subtree.children if subtree else tree  # in case of item is the root element

    def fetch_geojson(self, item: WambachersNode) -> None:
        logger.debug('Fetch polygon data for %s', item)
        response = requests.get(item.boundaries_url)
        assert response.status_code == 200, f'Bad request, status {response.status_code}'
        logger.debug('Unpack polygon data for %s', item)
        with gzip.open(BytesIO(response.content)) as zipfile:
            logger.debug('Save polygon data in cache for %s', item)
            with open(item.geojson_path, 'wb') as dst:
                dst.write(zipfile.read())

    def _parse(self, feature) -> Feature:
        def langs(tags: Dict[str, str]) -> Dict[str, str]:
            return {lang: tags.get(f'name:{lang}', '(empty)') for lang in settings.ALLOWED_LANGUAGES}

        assert feature['type'] == 'Feature'
        result = Feature(
            geometry=GEOSGeometry(json.dumps(feature['geometry'])),
            osm_id=abs(int(feature['properties']['osm_id'])),
            wikidata_id=feature['properties']['all_tags']['wikidata'],
            level=feature['properties']['admin_level'],
            boundary=feature['properties']['boundary'],
            name=feature['properties']['name'],
            path=[abs(int(x)) for x in feature['properties']['parents'].split(',')]
            if feature['properties']['parents'] else [],
            alpha3=feature['properties']['all_tags'].get('ISO3166-1:alpha3'),
            timezone=feature['properties']['all_tags'].get('timezone'),
            lang=langs(feature['properties']['all_tags'])
        )
        if isinstance(result.geometry, Polygon):
            result.geometry = MultiPolygon(result.geometry)
        return result

    def load(self, item: WambachersNode) -> Feature:
        cache = item.geojson_path
        if not cache.exists():
            settings.GEOJSON_DIR.mkdir(exist_ok=True)
            logger.debug('Missing cache for %s', item)
            self.fetch_geojson(item)
        with open(cache, 'r', encoding='utf-8') as src:
            data = json.loads(src.read())
            logger.debug('GeoJSON for %s was parsed', item)
            assert data['type'] == 'FeatureCollection', f'Found unknown type: {data["type"]}'
            return [self._parse(feature) for feature in data['features']][0]
