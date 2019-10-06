import factory
from django.contrib.gis.geos import Point, MultiPoint
from factory import SubFactory
from factory.django import ImageField, DjangoModelFactory

from maps.factories import GameFactory, RegionFactory
from puzzle.models import Puzzle, PuzzleRegion


class PuzzleFactory(GameFactory):
    default_positions = MultiPoint((Point(0, 0), Point(1, 1)))
    image = ImageField(from_path='static/images/world/default_80.png')

    class Meta:
        model = Puzzle

    @factory.post_generation
    def translations(self, create, extracted, **kwargs):
        for translation in self.translations.all():
            translation.name = f'{translation.name}-{translation.language_code}'
            translation.save()


class PuzzleRegionFactory(DjangoModelFactory):
    region = SubFactory(RegionFactory)
    puzzle = SubFactory(PuzzleFactory)
    is_solved = False

    class Meta:
        model = PuzzleRegion
