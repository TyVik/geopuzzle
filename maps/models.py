import json
import os
import time
from zipfile import ZipFile

import requests
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from hvad.manager import TranslationManager
from typing import List, Dict

from django.conf import settings
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from hvad.models import TranslatableModel, TranslatedFields
from hvad.utils import load_translation
from io import BytesIO

from maps.converter import encode_geometry
from maps.fields import ExternalIdField
from maps.infobox import query_by_wikidata_id

ZOOMS = (
    (3, 'world'),
    (4, 'large country'),
    (5, 'big country'),
    (6, 'country'),
    (7, 'small country'),
    (8, 'little country'),
    (9, 'region'),
)


class RegionManager(TranslationManager):
    def get_queryset(self):
        return super(RegionManager, self).get_queryset().defer('polygon')


class Region(TranslatableModel):
    title = models.CharField(max_length=128)
    polygon = MultiPolygonField(geography=True)
    parent = models.ForeignKey('Region', null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    wikidata_id = ExternalIdField(max_length=20, link='https://www.wikidata.org/wiki/{id}', null=True)
    osm_id = models.PositiveIntegerField(unique=True)
    osm_data = JSONField(default={})
    is_enabled = models.BooleanField(default=True)

    translations = TranslatedFields(
        name=models.CharField(max_length=120),
        infobox=JSONField(default={})
    )

    objects = RegionManager()
    caches = {
        'polygon_gmap': 'region{id}gmap',
        'polygon_bounds': 'region{id}bounds',
        'polygon_strip': 'region{id}strip',
    }

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.title

    @property
    def polygon_bounds(self) -> List:
        cache_key = self.caches['polygon_bounds'].format(id=self.id)
        points = cache.get(cache_key)
        if points is None:
            points = self.polygon.extent
            cache.set(cache_key, points, timeout=None)
        return points

    @property
    def polygon_strip(self) -> List:
        cache_key = self.caches['polygon_strip'].format(id=self.id)
        result = cache.get(cache_key)
        if result is None:
            simplify = self.polygon.simplify(0.01, preserve_topology=True)
            result = encode_geometry(simplify, min_points=15)
            cache.set(cache_key, result, timeout=None)
        return result

    @property
    def polygon_gmap(self) -> List:
        cache_key = self.caches['polygon_gmap'].format(id=self.id)
        result = cache.get(cache_key)
        if result is None:
            result = encode_geometry(self.polygon)
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
        return {'infobox': self.strip_infobox, 'polygon': self.polygon_strip, 'id': self.id}

    def import_osm_polygon(self) -> None:
        def content():
            cache = os.path.join(settings.GEOJSON_DIR, '{}.geojson'.format(self.osm_id))
            if not os.path.exists(cache):
                url = settings.OSM_URL.format(id=self.osm_id, key=settings.OSM_KEY, level=2 if self.country.is_global else 4)
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

        geojson = content()
        self.polygon = GEOSGeometry(json.dumps(geojson['features'][0]['geometry']))
        simplify = self.polygon.simplify(0.01, preserve_topology=True)
        if not isinstance(simplify, MultiPolygon):
            simplify = MultiPolygon(simplify)
        self.polygon = simplify
        self.save()

    def update_infobox_by_wikidata_id(self) -> None:
        time.sleep(5)  # protection for DDoS
        country_id = self.parent.wikidata_id
        rows = query_by_wikidata_id(country_id=country_id, item_id=self.wikidata_id)
        for lang, infobox in rows.items():
            trans = load_translation(self, lang, enforce=True)
            trans.master = self
            trans.infobox = infobox
            trans.name = infobox.get('name', '')
            trans.save()


class RegionTranslationProxy(models.Model):
    name = models.CharField(max_length=120)
    infobox = JSONField(default={})
    language_code = models.CharField(max_length=2)
    master = models.ForeignKey(Region)

    class Meta:
        managed = False
        db_table = 'maps_region_translation'


@receiver(post_save, sender=Region, dispatch_uid="clear_region_cache")
def clear_region_cache(sender, instance: Region, **kwargs):
    for key in instance.caches:
        cache.delete(instance.caches[key].format(id=instance.id))


class Game(TranslatableModel):
    image = models.ImageField(upload_to='upload/puzzles', blank=True, null=True)
    slug = models.CharField(max_length=15, db_index=True)
    center = PointField(geography=True)
    zoom = models.PositiveSmallIntegerField(choices=ZOOMS)
    is_published = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False)
    regions = models.ManyToManyField(Region)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        raise NotImplementedError

    def get_init_params(self) -> Dict:
        return {
            'zoom': self.zoom,
            'center': {'lng': self.center.coords[0], 'lat': self.center.coords[1]}
        }
