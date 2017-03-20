from django import forms
from django.contrib.gis.geos import Point

from maps.views import MapForm


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


class QuizInfoboxForm(MapForm):
    params = forms.CharField()

    def clean_params(self):
        return self.cleaned_data['params'].split(',')

    def json(self):
        result = []
        for area in self.areas():
            k = {'id': area.id}
            for param in self.cleaned_data['params']:
                value = area.infobox['capital']['name'] if param == 'capital' else area.infobox.get(param, None)
                k[param] = value
            result.append(k)
        return result
