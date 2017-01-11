from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.geos import Polygon
from django.db import models


class Meta(models.Model):
    name = models.CharField(max_length=15)
    table_name = models.CharField(max_length=15)
    center = PointField(geography=True)
    position = PointField(geography=True)
    zoom = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class World(models.Model):
    name = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    polygon = MultiPolygonField(geography=True)
    answer = PolygonField(geography=True)

    def __str__(self):
        return self.name

    def recalc_answer(self):
        diff = (-1, -1, 1, 1)
        extent = self.polygon.extent
        points = [extent[i] + diff[i] for i in range(4)]
        self.answer = Polygon(((points[0], points[1]), (points[2], points[1]), (points[2], points[3]), (points[0], points[3]), (points[0], points[1])))
        self.save()
