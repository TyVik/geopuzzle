from typing import List, Dict

from django import forms
from django.contrib.gis.geos import Point

from maps.forms import RegionForm


class PointContainsForm(forms.Form):
    lat = forms.FloatField()
    lng = forms.FloatField()

    def __init__(self, area, *args, **kwargs):
        self.area = area
        super(PointContainsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PointContainsForm, self).clean()
        point = Point(cleaned_data.get('lng'), cleaned_data.get('lat'))
        if not self.area.polygon.contains(point):
            raise forms.ValidationError('Point not in polygons')


class QuizInfoboxForm(RegionForm):
    params = forms.CharField()

    def clean_params(self) -> List:
        return self.cleaned_data['params'].split(',')

    def json(self) -> Dict:
        def extract_capital(capital) -> str:
            return capital['name'] if isinstance(capital, dict) else capital

        questions = []
        founded = []
        for region in self.regions:
            if region.infobox is None:
                founded.append(region)
            for param in self.cleaned_data['params']:
                if param == 'capital':
                    capital = region.infobox.get('capital', None)
                    value = region.infobox.get('name', None) if capital is None else extract_capital(capital)
                else:
                    value = region.infobox.get(param, None)
                if value is not None:
                    k[param] = value

            # if question has not values - set them as founded
            if k != {}:
                k = {'id': region.id}
                questions.append(k)
            else:
                founded.append(region)
        return {'questions': questions, 'founded': founded}
