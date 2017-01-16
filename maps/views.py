import json

from django import forms
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from maps.models import Country, Area, DIFFICULTY_LEVELS


class MapForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), to_field_name='slug')
    id = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=False)
    difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVELS, required=False, initial=1)
    count = forms.IntegerField(required=False, initial=3)

    def clean_country(self):
        self.meta = self.cleaned_data.get('country', None)
        return self.meta

    def areas(self):
        if len(self.cleaned_data['id']) > 0:
            return self.cleaned_data['id']

        queryset = Area.objects.filter(country=self.cleaned_data['country']).exclude(difficulty=0).order_by('?')
        if self.cleaned_data['difficulty'] != '':
            queryset = queryset.filter(difficulty__lte=int(self.cleaned_data['difficulty']))
        count = self.cleaned_data['count'] if self.cleaned_data['count'] is not None else self.meta.default_count
        if count > 0:
            queryset = queryset[:count]
        return queryset


def index(request):
    return render(request, 'index.html', {'countries': Country.objects.exclude(slug='world').order_by('name').all()})


def maps(request, name):
    params = request.GET.copy()
    params['country'] = name
    form = MapForm(params)
    if not form.is_valid():
        return HttpResponseBadRequest(json.dumps(form.errors))
    areas = form.areas()
    country = {'zoom': form.meta.zoom, 'position': form.meta.position, 'center': form.meta.center}
    question = ', '.join([country.polygon.geojson for country in areas])
    answer = [list([list(country.answer.coords[0]), list(country.answer.coords[1])]) for country in areas]
    return render(request, 'maps/map.html', context={'question': question, 'country': country, 'answer': answer})
