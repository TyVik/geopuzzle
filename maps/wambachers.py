import json
import logging
import os
from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List
from zipfile import ZipFile

import requests
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry


logger = logging.getLogger('wambachers')


@dataclass
class WambachersNode:
    id: int
    text: str
    level: int


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
    osm_id: int
    features: List

    def __init__(self, osm_id: int):
        super(Wambachers, self).__init__()
        self.osm_id = osm_id
        logger.debug('Created Wambachers service with OSM ID %s', osm_id)

    def fetch_items_list(self) -> List[WambachersNode]:
        params = {'caller': 'boundaries-4.6.4', 'database': 'planet3', 'parent': self.osm_id, 'addi': 810, 'debug': 3}
        headers = {
            'Referer': 'https://wambachers-osm.website/boundaries/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'JSESSIONID=node01ln7zb8ljtnbacctakke8yb6s49.node0; osm_boundaries_map='
                      '1%7C40.65536999999962%7C45.25161549584642%7C10%7C0BT%7Copen; osm_boundaries_base='
                      '4%7Cfalse%7Cjson%7Czip%7Cnull%7Cfalse%7Clevels%7Cland%7C4.3%7Ctrue%7C3',
        }
        response = requests.post('https://wambachers-osm.website/boundaries/getJsTree7',
                                 params=params, headers=headers)
        return [WambachersNode(id=item['id'], text=item['text'], level=item['data']['admin_level'])
                for item in response.json()]

    @property
    def geojson_path(self) -> str:
        return os.path.join(settings.GEOJSON_DIR, f'{self.osm_id}.geojson')

    def fetch_geojson(self, osm_id, level):
        logger.debug('Fetch polygon data for %s', osm_id)
        url = settings.OSM_URL.format(id=osm_id, key=settings.OSM_KEY, level=level)
        response = requests.get(url)
        assert response.status_code == 200, f'Bad request, status {response.status_code}'
        logger.debug('Unpack polygon data for %s', osm_id)
        zipfile = ZipFile(BytesIO(response.content))
        zip_names = zipfile.namelist()
        assert len(zip_names) == 1, 'Too many geometries'
        filename = zip_names.pop()
        logger.debug('Save polygon data in cache for %s', osm_id)
        with open(self.geojson_path, 'wb') as dst:
            dst.write(zipfile.open(filename).read())

    def _parse(self, feature) -> Feature:
        def langs(tags: Dict[str, str]) -> Dict[str, str]:
            return {lang: tags.get(f'name:{lang}', '(empty)') for lang in settings.ALLOWED_LANGUAGES}

        assert feature['type'] == 'Feature'
        return Feature(
            geometry=GEOSGeometry(json.dumps(feature['geometry'])),
            osm_id=int(feature['properties']['id']),
            wikidata_id=feature['properties']['wikidata'],
            level=feature['properties']['admin_level'],
            boundary=feature['properties']['boundary'],
            name=feature['properties']['name'],
            path=[int(x) for x in feature['properties']['rpath'].split(',')],
            alpha3=feature['properties']['alltags'].get('ISO3166-1:alpha3'),
            timezone=feature['properties']['alltags'].get('timezone'),
            lang=langs(feature['properties']['alltags'])
        )

    def load(self, level: int) -> None:
        cache = self.geojson_path
        if not os.path.exists(cache):
            logger.debug('Missing cache for %s', self.osm_id)
            self.fetch_geojson(self.osm_id, level)
        with open(cache, 'r') as src:
            data = json.loads(src.read())
            logger.debug('GeoJSON for %s was parsed', self.osm_id)
            assert data['type'] == 'FeatureCollection', f'Found unknown type: {data["type"]}'
            self.features = [self._parse(feature) for feature in data['features']]
        assert len(self.features) == 1
