import json
import random
import time
from zipfile import ZipFile

import requests
from django.contrib.gis.geos import GEOSGeometry
from hvad.manager import TranslationManager
from typing import List, Dict, Tuple

from django.conf import settings
from django.contrib.gis.db.models import MultiPointField
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from hvad.models import TranslatableModel, TranslatedFields
from hvad.utils import load_translation
from io import BytesIO

from maps.converter import encode_coords
from maps.fields import ExternalIdField
from maps.infobox import query_by_wikidata_id

DIFFICULTY_LEVELS = (
    (0, 'disabled'),
    (1, 'easy'),
    (2, 'normal'),
    (3, 'hard'),
)

ZOOMS = (
    (3, 'world'),
    (4, 'large country'),
    (5, 'big country'),
    (6, 'country'),
    (7, 'small country'),
    (8, 'little country'),
    (9, 'region'),
)


class Country(TranslatableModel):
    image = models.ImageField(upload_to='countries', blank=True, null=True)
    slug = models.CharField(max_length=15, db_index=True)
    center = PointField(geography=True)
    default_positions = MultiPointField(geography=True)
    zoom = models.PositiveSmallIntegerField(choices=ZOOMS)
    is_published = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False)
    wikidata_id = ExternalIdField(max_length=15, link='https://www.wikidata.org/wiki/{id}')

    translations = TranslatedFields(
        name = models.CharField(max_length=15)
    )

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __init__(self, *args, **kwargs):
        self.__default_positions = []
        super(Country, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('puzzle_map', args=(self.slug,))

    def get_init_params(self) -> Dict:
        return {
            'zoom': self.zoom,
            'center': {'lng': self.center.coords[0], 'lat': self.center.coords[1]}
        }

    def pop_position(self) -> Tuple:
        if len(self.__default_positions) == 0:
            self.__default_positions = self.default_positions[:]
            random.shuffle(self.__default_positions)
        return self.__default_positions.pop().coords


class AreaManager(TranslationManager):
    def get_queryset(self):
        return super(AreaManager, self).get_queryset().defer('polygon')


class Area(TranslatableModel):
    country = models.ForeignKey(Country)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVELS, default=0)
    polygon = MultiPolygonField(geography=True)
    wikidata_id = ExternalIdField(max_length=15, null=True, blank=True, link='https://www.wikidata.org/wiki/{id}')
    osm_id = ExternalIdField(max_length=15, null=True, blank=True)

    objects = AreaManager()
    translations = TranslatedFields(
        name = models.CharField(max_length=50),
        infobox = JSONField(null=True, blank=True)
    )

    caches = {
        'polygon_gmap': 'area{id}gmap',
        'polygon_bounds': 'area{id}bounds',
        'polygon_strip': 'area{id}strip',
    }

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return '{}?id={}'.format(reverse('quiz_map', args=(self.country.slug,)), self.id)

    @property
    def polygon_bounds(self) -> List:
        cache_key = self.caches['polygon_bounds'].format(id=self.id)
        points = cache.get(cache_key)
        if points is None:
            diff = (-1, -1, 1, 1)
            extent = self.polygon.extent
            scale = 1.0 / (self.country.zoom - 2)
            points = [extent[i] + diff[i] * scale for i in range(4)]
            cache.set(cache_key, points, timeout=None)
        return points

    @property
    def polygon_strip(self) -> List:
        cache_key = self.caches['polygon_strip'].format(id=self.id)
        result = cache.get(cache_key)
        if result is None:
            result = []
            simplify = self.polygon.simplify(0.01)
            for polygon in simplify:
                if isinstance(polygon.coords[0][0], float):
                    result.append(encode_coords(polygon.coords))
                else:
                    result.append(encode_coords(polygon.coords[0]))
                    if len(polygon.coords) > 1:
                        result.append(encode_coords(polygon.coords[1]))
            cache.set(cache_key, result, timeout=None)
        return result

    @property
    def polygon_gmap(self) -> List:
        cache_key = self.caches['polygon_gmap'].format(id=self.id)
        result = cache.get(cache_key)
        if result is None:
            result = []
            for polygon in self.polygon:
                result.append(encode_coords(polygon.coords[0]))
                if len(polygon.coords) > 1:
                    result.append(encode_coords(polygon.coords[1]))
            cache.set(cache_key, result, timeout=None)
        return result

    @property
    def center(self) -> List:
        # http://lists.osgeo.org/pipermail/postgis-users/2007-February/014612.html
        return list(self.polygon.centroid)

    def infobox_status(self) -> Dict:
        fields = ('name', 'wiki', 'capital', 'coat_of_arms', 'flag')
        result = {} if self.infobox is None else {field: field in self.infobox for field in fields}
        result['capital'] = result.get('capital') and isinstance(self.infobox['capital'], dict)
        return result

    @property
    def strip_infobox(self) -> Dict:
        result = self.infobox
        result.pop('geonamesID', None)
        if 'capital' in result and isinstance(result['capital'], dict):
            del (result['capital']['id'])
        return result

    @property
    def full_info(self) -> Dict:
        return {'infobox': self.strip_infobox, 'polygon': self.polygon_gmap, 'id': self.id}

    def import_osm_polygon(self) -> None:
        url = settings.OSM_URL.format(id=self.osm_id, key=settings.OSM_KEY, level=2 if self.country.is_global else 4)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Bad request')
        zipfile = ZipFile(BytesIO(response.content))
        zip_names = zipfile.namelist()
        if len(zip_names) != 1:
            raise Exception('Too many geometries')
        filename = zip_names.pop()
        geojson = json.loads(zipfile.open(filename).read().decode())
        self.polygon = GEOSGeometry(json.dumps(geojson['features'][0]['geometry']))
        self.save()

    def update_infobox_by_wikidata_id(self) -> None:
        time.sleep(5)  # protection for DDoS
        country_id = self.country.wikidata_id if not self.country.is_global else None
        rows = query_by_wikidata_id(country_id=country_id, item_id=self.wikidata_id)
        for lang, infobox in rows.items():
            trans = load_translation(self, lang, enforce=True)
            trans.master = self
            trans.infobox = infobox
            trans.name = infobox.get('name', '')
            trans.save()


@receiver(post_save, sender=Area, dispatch_uid="clear_area_cache")
def clear_area_cache(sender, instance, **kwargs):
    for key in instance.caches:
        cache.delete(instance.caches[key].format(id=instance.id))
