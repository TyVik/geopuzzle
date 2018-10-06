from django.contrib.gis.geos import Point, MultiPoint
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText


class GameFactory(DjangoModelFactory):
    is_published = True
    center = Point(0, 0)
    zoom = 3
    slug = FuzzyText()

