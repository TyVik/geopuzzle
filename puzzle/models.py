import random
from typing import Tuple

from django.conf import settings
from django.contrib.gis.db.models import MultiPointField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from maps.models import Game, GameTranslation


class Puzzle(Game):
    default_positions = MultiPointField(geography=True)

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


class PuzzleTranslation(GameTranslation):
    master = models.ForeignKey(Puzzle, related_name='translations', editable=False)

    class Meta:
        unique_together = ('language_code', 'master')
        db_table = 'puzzle_puzzle_translation'


@receiver(post_save, sender=Puzzle)
def attach_translations(sender, instance, created, **kwargs):
    if created:
        common = {'master': instance, 'name': instance.slug}
        for lang, _ in settings.LANGUAGES:
            PuzzleTranslation.objects.create(language_code=lang, **common)
