import random
import time
from typing import List, Dict, Tuple

from django.contrib.gis.db.models import MultiPointField
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import MultiPoint
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from hvad.models import TranslatableModel, TranslatedFields
from hvad.utils import load_translation

from maps.converter import encode_coords
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
    position = PointField(geography=True)
    default_positions = MultiPointField(geography=True, null=True)
    zoom = models.PositiveSmallIntegerField(choices=ZOOMS)
    default_count = models.PositiveSmallIntegerField(default=0)  # deprecated
    sparql = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False)
    wikidata_id = models.CharField(max_length=15)

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
        return reverse('maps_map', args=(self.slug,))

    def get_init_params(self) -> Dict:
        return {
            'zoom': self.zoom,
            'center': {'lng': self.center.coords[0], 'lat': self.center.coords[1]}
        }

    def pop_position(self) -> Tuple:
        if self.default_positions is None:
            return self.position.coords
        if len(self.__default_positions) == 0:
            self.__default_positions = self.default_positions[:]
            random.shuffle(self.__default_positions)
        return self.__default_positions.pop().coords


class Area(TranslatableModel):
    country = models.ForeignKey(Country)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVELS, default=0)
    polygon = MultiPolygonField(geography=True)
    answer = MultiPointField(geography=True, null=True)
    wikidata_id = models.CharField(max_length=15, null=True, blank=True)

    translations = TranslatedFields(
        name = models.CharField(max_length=50),
        infobox = JSONField(null=True, blank=True)
    )

    caches = {
        'polygon_gmap': 'area{id}gmap',
    }

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return '{}?id={}'.format(reverse('maps_map', args=(self.country.slug,)), self.id)

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

    @property
    def strip_infobox(self) -> Dict:
        result = self.infobox
        del (result['geonamesID'])
        if 'capital' in result:
            del (result['capital']['id'])
        return result

    def _update_infobox(self, rows):
        for lang, infobox in rows.items():
            trans = load_translation(self, lang, enforce=True)
            trans.master = self
            trans.infobox = infobox
            trans.name = infobox.get('name', '')
            trans.save()

    def update_infobox_by_wikidata_id(self) -> None:
        time.sleep(5)  # protection for DDoS
        country_id = self.country.wikidata_id if not self.country.is_global else None
        rows = query_by_wikidata_id(country_id=country_id, item_id=self.wikidata_id)
        self._update_infobox(rows)

    def recalc_answer(self) -> None:
        diff = (-1, -1, 1, 1)
        extent = self.polygon.extent
        scale = 1.0 / (self.country.zoom - 2)
        points = [extent[i] + diff[i] * scale for i in range(4)]
        self.answer = MultiPoint(Point(points[0], points[1]), Point(points[2], points[3]))
        self.save()


@receiver(post_save, sender=Area, dispatch_uid="clear_area_cache")
def clear_area_cache(sender, instance, **kwargs):
    for key in instance.caches:
        cache.delete(instance.caches[key].format(id=instance.id))
