import json
import logging
import os
from zipfile import ZipFile

import requests
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from typing import List, Dict

from django.conf import settings
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models import Exists, OuterRef, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import get_language
from io import BytesIO

from common.cachable import CacheablePropertyMixin, cacheable
from maps.converter import encode_geometry
from maps.fields import ExternalIdField
from maps.infobox import query_by_wikidata_id
from users.models import User

ZOOMS = (
    (3, 'world'),
    (4, 'large country'),
    (5, 'big country'),
    (6, 'country'),
    (7, 'small country'),
    (8, 'little country'),
    (9, 'region'),
)
fetch_logger = logging.getLogger('fetch_region')


class RegionManager(models.Manager):
    def get_queryset(self):
        return super(RegionManager, self).get_queryset().defer('polygon')


class Region(CacheablePropertyMixin, models.Model):
    title = models.CharField(max_length=128)
    polygon = MultiPolygonField(geography=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    wikidata_id = ExternalIdField(max_length=20, link='https://www.wikidata.org/wiki/{id}', null=True)
    osm_id = models.PositiveIntegerField(unique=True)
    osm_data = JSONField(default={})
    is_enabled = models.BooleanField(default=True)

    objects = RegionManager()
    caches = {
        'polygon_center': 'region{id}center',
        'polygon_gmap': 'region{id}gmap',
        'polygon_bounds': 'region{id}bounds',
        'polygon_strip': 'region{id}strip',
        'polygon_infobox': 'region{id}infobox',
    }

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def __init__(self, *args, **kwargs):
        super(Region, self).__init__(*args, **kwargs)

    @property
    @cacheable
    def polygon_bounds(self) -> List:
        return self.polygon.extent

    @property
    def _strip_polygon(self):
        precision = 0.01 + 0.004 * (self.polygon.area / 10.0)
        return self.polygon.simplify(precision, preserve_topology=True)

    @property
    @cacheable
    def polygon_strip(self) -> List:
        simplify = self._strip_polygon
        return encode_geometry(simplify, min_points=10)

    @property
    @cacheable
    def polygon_gmap(self) -> List:
        precision = 0.005 + 0.001 * (self.polygon.area / 100.0)
        simplify = self.polygon.simplify(precision, preserve_topology=True)
        return encode_geometry(simplify)

    @property
    @cacheable
    def polygon_center(self) -> List:
        # http://lists.osgeo.org/pipermail/postgis-users/2007-February/014612.html
        def calc_polygon(strip, force):
            def calc_part(result, subpolygon):
                for point in subpolygon.coords[0]:
                    result['count'] += 1
                    result['lat'] += point[0]
                    result['lng'] += point[1]
                return result

            result = {'lat': 0.0, 'lng': 0.0, 'count': 0}
            if isinstance(strip, MultiPolygon):
                for part in strip:
                    if force or part.num_points > 10:
                        result = calc_part(result, part)
            else:
                result = calc_part(result, strip)
            return result

        result = calc_polygon(self._strip_polygon, force=False)
        if result['count'] == 0:
            result = calc_polygon(self._strip_polygon, force=True)
        return [result['lat'] / result['count'], result['lng'] / result['count']]

    def infobox_status(self, lang: str) -> Dict:
        fields = ('name', 'wiki', 'capital', 'coat_of_arms', 'flag')
        trans = self.load_translation(lang)
        result = {field: field in trans.infobox for field in fields}
        result['capital'] = result.get('capital') and isinstance(trans.infobox['capital'], dict)
        return result

    @property
    @cacheable
    def polygon_infobox(self) -> Dict:
        def get_marker(infobox):
            by_capital = infobox.get('capital', {})
            if 'lat' in by_capital and 'lon' in by_capital:
                return {'lat': by_capital['lat'], 'lon': by_capital['lon']}
            else:
                center = self.polygon_center
                return {'lat': center[1], 'lon': center[0]}

        result = {}
        for trans in self.translations.all():
            infobox = trans.infobox
            infobox.pop('geonamesID', None)
            if isinstance(infobox.get('capital'), dict):
                del (infobox['capital']['id'])
            infobox['marker'] = get_marker(infobox)
            result[trans.language_code] = infobox
        return result

    def full_info(self, lang: str) -> Dict:
        return {'infobox': self.polygon_infobox[lang], 'polygon': self.polygon_gmap, 'id': self.id}

    def json(self, lang: str) -> Dict:
        translation = self.load_translation(lang)
        result = {'id': str(self.id), 'name': translation.name, 'items': self.items(lang)}
        result['items_exists'] = len(result['items']) > 0
        return result

    def items(self, lang: str) -> List[Dict]:
        child_query = Region.objects.filter(parent_id=OuterRef('pk'))
        return [{'id': str(x.id), 'name': x.lang, 'items_exists': x.items_exists} for x in
                self.region_set
                    .filter(translations__language_code=lang)
                    .annotate(items_exists=Exists(child_query), lang=F('translations__name'))
                    .order_by('lang')
                    .distinct()]

    def fetch_polygon(self) -> None:
        def content():
            cache = os.path.join(settings.GEOJSON_DIR, '{}.geojson'.format(self.osm_id))
            if not os.path.exists(cache):
                url = settings.OSM_URL.format(id=self.osm_id, key=settings.OSM_KEY, level=self.osm_data['level'])
                fetch_logger.info(f'Download from {url}')
                response = requests.get(url)
                if response.status_code != 200:
                    raise Exception('Bad request')
                zipfile = ZipFile(BytesIO(response.content))
                zip_names = zipfile.namelist()
                if len(zip_names) != 1:
                    raise Exception('Too many geometries')
                filename = zip_names.pop()
                with open(cache, 'wb') as c:
                    c.write(zipfile.open(filename).read())
            with open(cache, 'r') as c:
                return json.loads(c.read())

        def update_self(properties, geometry, type):
            def extract_data(properties):
                result = {'level': int(properties['admin_level'])}
                fields = ['boundary', 'ISO3166-1:alpha3', 'timezone']
                for field in fields:
                    result[field] = properties['alltags'].get(field, None)
                return result

            self.title = properties['name']
            self.polygon = GEOSGeometry(json.dumps(geometry))
            self.wikidata_id = properties.get('wikidata')
            self.osm_id = properties['id']
            self.osm_data = extract_data(properties)

        fetch_logger.info(f'Update polygon: {self.id}')
        feature = content()['features'][0]
        update_self(**feature)
        self.save()

        for lang in settings.ALLOWED_LANGUAGES:
            trans = self.load_translation(lang)
            trans.master = self
            trans.name = self.title
            trans.save()

    def fetch_items_list(self) -> Dict:
        params = {'caller': 'boundaries-4.3.14', 'database': 'planet3', 'parent': self.osm_id}
        headers = {
            'Referer': 'https://wambachers-osm.website/boundaries/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'JSESSIONID=node01ln7zb8ljtnbacctakke8yb6s49.node0; osm_boundaries_map=1%7C40.65536999999962%7C45.25161549584642%7C10%7C0BT%7Copen; osm_boundaries_base=4%7Cfalse%7Cjson%7Czip%7Cnull%7Cfalse%7Clevels%7Cland%7C4.3%7Ctrue%7C3',
        }
        fetch_logger.info(f'Get items: {self.id}')
        response = requests.post('https://wambachers-osm.website/boundaries/getJsTree6', params=params, headers=headers)
        items = response.json()
        fetch_logger.info(f'Count items for {self.id}: {len(items)}')
        return items

    def fetch_items(self) -> None:
        for item in self.fetch_items_list():
            if item['data']['admin_level'] >= 8:
                continue
            region, _ = Region.objects.get_or_create(osm_id=item['id'], defaults={'parent': self, 'osm_data': {'level': item['data']['admin_level']}})
            region.fetch_polygon()
            region.fetch_infobox()

    def fetch_infobox(self) -> None:
        fetch_logger.info(f'Get infobox: {self.wikidata_id}')
        if self.wikidata_id is None or self.wikidata_id == '':
            rows = {lang: {} for lang in settings.ALLOWED_LANGUAGES}
        else:
            wikidata_id = None if self.parent is None else self.parent.wikidata_id
            rows = query_by_wikidata_id(country_id=wikidata_id, item_id=self.wikidata_id)
        for lang, infobox in rows.items():
            fetch_logger.info(f'Update infobox: {lang}')
            if 'name' not in infobox:
                infobox['name'] = self.title
            trans = self.load_translation(lang)
            trans.master = self
            trans.infobox = infobox
            trans.name = infobox['name']
            trans.save()

    @property
    def translation(self):
        return self.load_translation(get_language())

    def load_translation(self, lang):
        result = self.translations.filter(language_code=lang).first()
        if result is None:
            result = RegionTranslation.objects.create(language_code=lang, master=self, name='(empty)')
        return result


class RegionTranslation(models.Model):
    name = models.CharField(max_length=120)
    infobox = JSONField(default={})
    language_code = models.CharField(max_length=15, choices=settings.LANGUAGES, db_index=True)
    master = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='translations', editable=False)

    class Meta:
        unique_together = ('language_code', 'master')
        db_table = 'maps_region_translation'


@receiver(post_save, sender=Region, dispatch_uid="clear_region_cache")
def clear_region_cache(sender, instance: Region, **kwargs):
    for key in instance.caches:
        cache.delete(instance.caches[key].format(id=instance.id))


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='games', blank=True, null=True)
    slug = models.CharField(max_length=15, db_index=True)
    center = PointField(geography=True)
    zoom = models.PositiveSmallIntegerField(choices=ZOOMS)
    is_published = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    regions = models.ManyToManyField(Region)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        raise NotImplementedError

    def load_translation(self, lang):
        return self.translations.filter(language_code=lang).first()

    @property
    def index(self) -> Dict:
        trans = self.load_translation(get_language())
        return {'image': self.image, 'slug': self.slug, 'name': trans.name}

    def get_init_params(self) -> Dict:
        return {
            'zoom': self.zoom,
            'center': {'lng': self.center.coords[0], 'lat': self.center.coords[1]},
            'options': {
                'streetViewControl': False,
                'mapTypeControl': False
            }
        }


class GameTranslation(models.Model):
    name = models.CharField(max_length=50)
    language_code = models.CharField(max_length=2, choices=settings.LANGUAGES, db_index=True)
    master = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='translations', editable=False)

    class Meta:
        unique_together = ('language_code', 'master')
        abstract = True
