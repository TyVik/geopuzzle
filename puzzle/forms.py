import base64
from random import uniform
from typing import Dict, List

from django import forms
from django.conf import settings
from django.contrib.gis.geos import MultiPoint, Point
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.forms import ModelForm, Field
from django.utils.translation import get_language

from common.utils import random_string
from maps.forms import RegionForm
from maps.models import Tag
from puzzle.models import PuzzleTranslation, Puzzle


class RegionContainsForm(forms.Form):
    north = forms.FloatField()
    east = forms.FloatField()
    south = forms.FloatField()
    west = forms.FloatField()

    def __init__(self, region, zoom, *args, **kwargs):
        self.region = region
        self.zoom = zoom
        super(RegionContainsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegionContainsForm, self).clean()
        data = {part: cleaned_data[part] for part in ['north', 'south', 'west', 'east']}
        diff = (-1, -1, 1, 1)
        extent = self.region.polygon_bounds
        scale = 1.0 / (self.zoom - 2)
        points = [extent[i] + diff[i] * scale for i in range(4)]
        if not (data['north'] < points[3] and data['south'] > points[1] and
                        data['east'] < points[2] and data['west'] > points[0]):
            raise forms.ValidationError('Point not in polygons')


class PuzzleForm(RegionForm):
    def json(self) -> Dict:
        qs = self.regions.filter(id__in=self.game.puzzleregion_set.filter(is_solved=False).
                                 values_list('region_id', flat=True))
        questions = [{
            'id': region.id,
            'name': region.translation.name,
            'polygon': region.polygon_strip,
            'center': region.polygon_center,
            'default_position': self.game.pop_position()}
            for region in qs]
        qs = self.regions.filter(id__in=self.game.puzzleregion_set.filter(is_solved=True).
                                 values_list('region_id', flat=True))
        solved = [region.full_info(get_language()) for region in qs]
        return {'questions': questions, 'solved': solved}


class BoundsField(Field):
    default_error_messages = {
        'invalid': 'Enter comma separated numbers only.',
    }

    def to_python(self, value):
        try:
            value = [float(item.strip()) for item in value.split(',') if item.strip()]
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'])
        return value


class PuzzleEditForm(ModelForm):
    bounds = BoundsField()
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Puzzle
        fields = ('regions', 'image', 'center', 'zoom', 'is_published', 'tags')

    def clean_image(self):
        format, imgstr = self.data.get('image').split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=f'{random_string()}.${ext}')

    def save(self, *args, **kwargs):
        def get_slug(slug: str) -> str:
            return random_string() if slug == '' else slug

        def get_positions(bounds: List[float], count: int) -> List:
            return [Point(uniform(bounds[1], bounds[3]), uniform(bounds[0], bounds[2]))
                    for _ in range(round(count * 2 / 3) + 1)]

        self.instance.slug = get_slug(self.instance.slug)
        self.instance.default_positions = MultiPoint(get_positions(
            self.cleaned_data['bounds'], len(self.cleaned_data['regions'])))
        return super(PuzzleEditForm, self).save(*args, **kwargs)

    def _save_m2m(self):
        super(PuzzleEditForm, self)._save_m2m()
        for lang in settings.ALLOWED_LANGUAGES:
            PuzzleTranslation.objects.update_or_create(
                master=self.instance, language_code=lang,
                defaults={'name': self.data.get(f'{lang}_name', '')})
