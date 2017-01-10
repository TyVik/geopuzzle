from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import PolygonField
from django.db import models


class Meta(models.Model):
    name = models.CharField(max_length=15)
    table_name = models.CharField(max_length=15)
    center = PointField(geography=True)
    position = PointField(geography=True)
    zoom = models.PositiveSmallIntegerField()


class World(models.Model):
    name = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    polygon = MultiPolygonField(geography=True)
    answer = PolygonField(geography=True)
