from typing import List

from django import forms
from django.core.exceptions import ValidationError
from django.forms import Field

from common.constants import GameQuestions
from common.utils import get_language
from maps.forms import RegionForm
from maps.models import RegionInterface
from .models import Puzzle


class RegionContainsForm(forms.Form):
    north = forms.FloatField()
    east = forms.FloatField()
    south = forms.FloatField()
    west = forms.FloatField()

    def __init__(self, area: RegionInterface, zoom: int, *args, **kwargs):
        self.region = area
        self.zoom = zoom
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        data = {part: cleaned_data[part] for part in ['north', 'south', 'west', 'east']}
        diff = (-1, -1, 1, 1)
        extent = self.region.polygon_bounds
        scale = 1.0 / (self.zoom - 2)
        points = [extent[i] + diff[i] * scale for i in range(4)]
        if not (data['north'] < points[3] and data['south'] > points[1] and
                data['east'] < points[2] and data['west'] > points[0]):
            raise forms.ValidationError('Point not in polygons')


class PuzzleForm(RegionForm):
    game: Puzzle

    def json(self) -> GameQuestions:
        qs = self.regions.filter(id__in=self.game.puzzleregion_set.filter(is_solved=False).
                                 values_list('region_id', flat=True))
        questions = [{
            'id': region.pk,
            'name': region.translation.name,
            'polygon': region.polygon_strip,
            'center': region.polygon_center,  # deprecated for Leaflet
            'default_position': self.game.pop_position()} for region in qs]
        qs = self.regions.filter(id__in=self.game.puzzleregion_set.filter(is_solved=True).
                                 values_list('region_id', flat=True))
        solved = [region.full_info(get_language()) for region in qs]
        return GameQuestions(questions=questions, solved=solved)


class BoundsField(Field):
    default_error_messages = {
        'invalid': 'Enter comma separated numbers only.',
    }

    def to_python(self, value: str) -> List[float]:
        try:
            return [float(item.strip()) for item in value.split(',') if item.strip()]
        except (ValueError, TypeError) as exception:
            raise ValidationError(self.error_messages['invalid']) from exception
