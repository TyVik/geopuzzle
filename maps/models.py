from django.utils.translation import ugettext as _
from django.contrib.gis.db.models import MultiPointField
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import MultiPoint
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse

from maps.infobox import query

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


class Country(models.Model):
    name = models.CharField(max_length=15)
    image = models.ImageField(upload_to='countries', blank=True)
    slug = models.CharField(max_length=15, db_index=True)
    center = PointField(geography=True)
    position = PointField(geography=True)
    zoom = models.PositiveSmallIntegerField(choices=ZOOMS)
    default_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('maps_map', args=(self.slug,))


class Area(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=50)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_LEVELS, default=0)
    polygon = MultiPolygonField(geography=True)
    answer = MultiPointField(geography=True, null=True)
    infobox = JSONField(null=True)

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '{}?id={}'.format(reverse('maps_map', args=(self.country.slug,)), self.id)

    def update_infobox(self):
        self.infobox = query(self.name)
        print(self.infobox)
        self.save()

    def recalc_answer(self):
        diff = (-1, -1, 1, 1)
        extent = self.polygon.extent
        scale = 1.0 / (self.country.zoom - 2)
        points = [extent[i] + diff[i] * scale for i in range(4)]
        self.answer = MultiPoint(Point(points[0], points[1]), Point(points[2], points[3]))
        self.save()
