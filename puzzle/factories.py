from django.contrib.gis.geos import Point, MultiPoint

from maps.factories import GameFactory


class PuzzleFactory(GameFactory):
    default_positions = MultiPoint((Point(0, 0), Point(1, 1)))

    class Meta:
        model = 'puzzle.Puzzle'
