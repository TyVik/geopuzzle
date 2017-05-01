import random
from typing import Dict, Tuple

from django.contrib.gis.db.models import PointField, MultiPointField
from django.db import models
from django.urls import reverse
from hvad.models import TranslatableModel, TranslatedFields

from maps.fields import ExternalIdField
from maps.models import ZOOMS, Region


class Puzzle(TranslatableModel):
    image = models.ImageField(upload_to='puzzles', blank=True, null=True)
    slug = models.CharField(max_length=15, db_index=True)
    center = PointField(geography=True)
    default_positions = MultiPointField(geography=True)
    zoom = models.PositiveSmallIntegerField(choices=ZOOMS)
    is_published = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False)
    wikidata_id = ExternalIdField(max_length=15, link='https://www.wikidata.org/wiki/{id}')
    regions = models.ManyToManyField(Region)

    translations = TranslatedFields(
        name=models.CharField(max_length=15)
    )

    class Meta:
        verbose_name = 'Puzzle'
        verbose_name_plural = 'Puzzles'

    def __init__(self, *args, **kwargs):
        self.__default_positions = []
        super(Puzzle, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return reverse('puzzle_map', args=(self.slug,))

    def get_init_params(self) -> Dict:
        return {
            'zoom': self.zoom,
            'center': {'lng': self.center.coords[0], 'lat': self.center.coords[1]}
        }

    def pop_position(self) -> Tuple:
        if len(self.__default_positions) == 0:
            self.__default_positions = self.default_positions[:]
            random.shuffle(self.__default_positions)
        return self.__default_positions.pop().coords
