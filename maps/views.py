import json

from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from maps.models import Country, Area, DIFFICULTY_LEVELS


class MapForm(forms.Form):
    difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVELS, required=False, initial=1)
    count = forms.IntegerField(required=False, initial=3)

    def __init__(self, *args, **kwargs):
        self.country = Country.objects.get(slug=kwargs.pop('slug', 'world'))
        super().__init__(*args, **kwargs)

    def areas(self):
        # return Map.objects.filter(meta_id=2, difficulty__gt=0, difficulty__lte=self.cleaned_data['difficulty'])[:self.cleaned_data['count']]
        return Area.objects.filter(country=self.country)


def maps(request, name):
    form = MapForm(request.GET, slug=name)
    if not form.is_valid():
        return HttpResponseBadRequest(json.dumps(form.errors))
    areas = form.areas()
    country = {'zoom': form.country.zoom, 'position': form.country.position, 'center': form.country.center}
    question = ', '.join([country.polygon.geojson for country in areas])
    answer = [list([list(country.answer.coords[0]), list(country.answer.coords[1])]) for country in areas]
    return render(request, 'maps/map.html', context={'question': question, 'country': country, 'answer': answer})
