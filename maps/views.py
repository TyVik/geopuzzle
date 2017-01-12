import json

from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from maps.models import Meta, Map, DIFFICULTY_LEVELS


class MapForm(forms.Form):
    difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVELS, required=False, initial=1)
    count = forms.IntegerField(required=False, initial=3)

    def countries(self):
        # return Map.objects.filter(meta_id=2, difficulty__gt=0, difficulty__lte=self.cleaned_data['difficulty'])[:self.cleaned_data['count']]
        return Map.objects.filter(meta_id=2)[:5]


def index(request):
    countries = Meta.objects.all()
    return render(request, 'maps/index.html', context={'countries': countries})


def maps(request, name):
    form = MapForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest(json.dumps(form.errors))
    countries = form.countries()
    world = Meta.objects.get(pk=2)
    meta = {'zoom': world.zoom, 'position': world.position, 'center': world.center}
    question = ', '.join([country.polygon.geojson for country in countries])
    answer = [list([list(country.answer.coords[0]), list(country.answer.coords[1])]) for country in countries]
    return render(request, 'maps/map.html', context={'question': question, 'meta': meta, 'answer': answer})
