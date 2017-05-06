import random
from typing import Tuple

from django.contrib.gis.db.models import MultiPointField
from django.db import models
from django.urls import reverse
from hvad.models import TranslatableModel, TranslatedFields

from maps.models import Game


class Puzzle(Game):
    default_positions = MultiPointField(geography=True)

    translations = TranslatedFields(
        name=models.CharField(max_length=15)
    )

    class Meta:
        verbose_name = 'Puzzle'
        verbose_name_plural = 'Puzzles'

    def __init__(self, *args, **kwargs):
        self.__default_positions = []
        super(Puzzle, self).__init__(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('puzzle_map', args=(self.slug,))

    def pop_position(self) -> Tuple:
        if len(self.__default_positions) == 0:
            self.__default_positions = self.default_positions[:]
            random.shuffle(self.__default_positions)
        return self.__default_positions.pop().coords
