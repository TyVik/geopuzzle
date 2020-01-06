from __future__ import annotations

from copy import deepcopy

from django.contrib.gis.geos import MultiPolygon, Polygon
from typing import List, Dict, Union, Tuple

from django.conf import settings
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import get_language

from common.cachable import cacheable
from common.constants import Point, LanguageEnumType
from ..constants import OsmRegionData
from ..converter import encode_geometry
from ..fields import ExternalIdField


class RegionInterface(object):
    @property  # type: ignore
    @cacheable
    def polygon_bounds(self) -> List:
        raise NotImplementedError

    @property  # type: ignore
    @cacheable
    def polygon_strip(self) -> List[str]:
        raise NotImplementedError

    @property  # type: ignore
    @cacheable
    def polygon_gmap(self) -> List[str]:
        raise NotImplementedError

    @property  # type: ignore
    @cacheable
    def polygon_center(self) -> List[float]:
        raise NotImplementedError

    @property  # type: ignore
    @cacheable
    def polygon_infobox(self) -> Dict:
        raise NotImplementedError

    def full_info(self, lang: str) -> Dict:
        return {'infobox': self.polygon_infobox[lang], 'polygon': self.polygon_gmap, 'id': self.id}


class RegionCacheMeta(type):
    def __new__(mcs, name, bases, dct):
        cls = type.__new__(mcs, name, bases, dct)
        for name, value in bases[0].__dict__.items():
            if name.startswith('polygon_'):
                setattr(cls, name, property(cacheable(cls.wrapper(name))))
        return cls

    def wrapper(cls, name: str):
        def wrapper(region_cache, *args, **kwargs):
            origin = Region.objects.get(pk=region_cache.id)
            return getattr(origin, name)
        wrapper.__name__ = name
        return wrapper


class RegionCache(RegionInterface, metaclass=RegionCacheMeta):
    def __init__(self, id: int):
        super(RegionCache, self).__init__()
        self.id = id


class RegionManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super(RegionManager, self).get_queryset().defer('polygon')


class Region(RegionInterface, models.Model):
    title = models.CharField(max_length=128)
    polygon = MultiPolygonField(geography=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    wikidata_id = ExternalIdField(max_length=20, link='https://www.wikidata.org/wiki/{id}', null=True)
    osm_id = models.PositiveIntegerField(unique=True)
    _osm_data = JSONField(default=dict, db_column='osm_data')
    is_enabled = models.BooleanField(default=True)

    objects = RegionManager()

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return f'{self.title} ({self.id})'

    def __init__(self, *args, **kwargs):
        super(Region, self).__init__(*args, **kwargs)

    @property  # type: ignore
    @cacheable
    def polygon_bounds(self) -> List:
        return self.polygon.extent

    @property
    def _strip_polygon(self) -> Union[Polygon, MultiPolygon]:
        precision = 0.01 + 0.004 * (self.polygon.area / 10.0)
        return self.polygon.simplify(precision, preserve_topology=True)

    @property  # type: ignore
    @cacheable
    def polygon_strip(self) -> List[str]:
        simplify = self._strip_polygon
        return encode_geometry(simplify, min_points=10)

    @property  # type: ignore
    @cacheable
    def polygon_gmap(self) -> List[str]:
        precision = 0.005 + 0.001 * (self.polygon.area / 100.0)
        simplify = self.polygon.simplify(precision, preserve_topology=True)
        return encode_geometry(simplify)

    @property  # type: ignore
    @cacheable
    def polygon_center(self) -> List[float]:
        # http://lists.osgeo.org/pipermail/postgis-users/2007-February/014612.html
        def calc_polygon(strip, force) -> Tuple[Point, int]:
            def calc_part(current, subtotal, subpolygon) -> Tuple[Point, int]:
                for point in subpolygon.coords[0]:
                    subtotal += 1
                    current['lat'] += point[0]
                    current['lng'] += point[1]
                return current, subtotal

            point = Point(lat=0.0, lng=0.0)
            count = 0
            if isinstance(strip, MultiPolygon):
                for part in strip:
                    if force or part.num_points > 10:
                        point, count = calc_part(point, count, part)
            else:
                point, count = calc_part(point, count, strip)
            return point, count

        point, count = calc_polygon(self._strip_polygon, force=False)
        if count == 0:
            point, count = calc_polygon(self._strip_polygon, force=True)
        return [point['lat'] / count, point['lng'] / count]

    def infobox_status(self, lang: LanguageEnumType) -> Dict[str, bool]:
        fields = ('name', 'wiki', 'capital', 'coat_of_arms', 'flag')
        trans = self.load_translation(lang)
        result = {field: field in trans.infobox for field in fields}
        result['capital'] = result.get('capital') and isinstance(trans.infobox['capital'], dict)
        return result

    @property  # type: ignore
    @cacheable
    def polygon_infobox(self) -> Dict:
        def get_marker(infobox) -> Point:
            by_capital = infobox.get('capital', {})
            if 'lat' in by_capital and 'lon' in by_capital:
                return Point(lat=by_capital['lat'], lng=by_capital['lon'])
            else:
                center = self.polygon_center
                return Point(lat=center[1], lng=center[0])

        result = {}
        for trans in self.translations.all():
            infobox = deepcopy(trans.infobox)
            infobox.pop('geonamesID', None)
            if isinstance(infobox.get('capital'), dict):
                del (infobox['capital']['id'])
            infobox['marker'] = get_marker(infobox)
            result[trans.language_code] = infobox
        return result

    @classmethod
    def caches(cls) -> List[str]:
        result = []
        for name in dir(cls):
            method = getattr(cls, name)
            if isinstance(method, property) and method.fget.__name__ == 'cache_wrapper':
                result.append(name)
        return result

    @property
    def osm_data(self) -> OsmRegionData:
        return OsmRegionData(**self._osm_data)

    @osm_data.setter
    def osm_data(self, data: OsmRegionData) -> None:
        self._osm_data = data

    @property
    def translation(self) -> RegionTranslation:
        return self.load_translation(get_language())

    def load_translation(self, lang: LanguageEnumType) -> RegionTranslation:
        result = self.translations.filter(language_code=lang).first()
        if result is None:
            result = RegionTranslation.objects.create(language_code=lang, master=self, name='(empty)')
        return result


class RegionTranslation(models.Model):
    name = models.CharField(max_length=120)
    infobox = JSONField(default=dict)
    language_code = models.CharField(max_length=15, choices=settings.LANGUAGES, db_index=True)
    master = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='translations', editable=False)

    class Meta:
        unique_together = ('language_code', 'master')
        db_table = 'maps_region_translation'


@receiver(post_save, sender=Region, dispatch_uid="clear_region_cache")
def clear_region_cache(sender, instance: Region, **kwargs):
    for key in instance.caches():
        cache.delete(settings.POLYGON_CACHE_KEY.format(func=key, id=instance.id))
