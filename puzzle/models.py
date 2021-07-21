import random
from typing import Tuple

from django.contrib.gis.db.models import MultiPointField
from django.db import models
from django.utils.translation import ugettext as _

from maps.fields import RegionsField
from maps.models import Game, GameTranslation, Region, Tag


class Puzzle(Game):
    default_positions = MultiPointField(geography=True)
    regions = RegionsField(Region, through='PuzzleRegion')
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = 'Puzzle'
        verbose_name_plural = 'Puzzles'

    def __init__(self, *args, **kwargs):
        self.__default_positions = []
        super().__init__(*args, **kwargs)

    @classmethod
    def name(cls) -> str:
        return _('Puzzle')

    @classmethod
    def description(cls) -> str:
        return _('In the Puzzle you need to drag the shape of the territory to the right place. Just like in '
                 'childhood we collected pictures piece by piece, so here you can collect a country from regions'
                 ' or whole continents from countries!')

    def pop_position(self) -> Tuple[float, float]:
        if len(self.__default_positions) == 0:
            self.__default_positions = self.default_positions[:]
            random.shuffle(self.__default_positions)
        return self.__default_positions.pop().coords


class PuzzleRegion(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=False)


class PuzzleTranslation(GameTranslation):
    master = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='translations', editable=False)

    class Meta:
        unique_together = ('language_code', 'master')
        db_table = 'puzzle_puzzle_translation'
