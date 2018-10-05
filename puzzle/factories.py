import factory
from django.contrib.gis.geos import Point, MultiPoint

from maps.factories import GameFactory
from puzzle.models import Puzzle


class PuzzleFactory(GameFactory):
    default_positions = MultiPoint((Point(0, 0), Point(1, 1)))

    class Meta:
        model = Puzzle

    @factory.post_generation
    def translations(self, create, extracted, **kwargs):
        for translation in self.translations.all():
            translation.name = f'{translation.name}-{translation.language_code}'
            translation.save()
