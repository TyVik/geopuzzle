from django.utils.translation import ugettext as _

from django import forms
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from maps.models import Country, Area, DIFFICULTY_LEVELS


class MapForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), to_field_name='slug')
    id = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=False)
    difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVELS, required=False, initial=1)
    count = forms.IntegerField(required=False, initial=3)
    lang = forms.ChoiceField(choices=settings.LANGUAGES, required=False, initial='en')

    def clean_country(self) -> Country:
        self.meta = self.cleaned_data.get('country', None)
        return self.meta

    def areas(self) -> QuerySet:
        if len(self.cleaned_data['id']) > 0:
            return self.cleaned_data['id']

        queryset = Area.objects.language(self.cleaned_data['lang']).filter(country=self.cleaned_data['country']).exclude(difficulty=0).order_by('?')
        if self.cleaned_data['difficulty'] != '':
            queryset = queryset.filter(difficulty=int(self.cleaned_data['difficulty']))
        count = self.cleaned_data['count'] if self.cleaned_data['count'] is not None else self.meta.default_count
        if count > 0:
            queryset = queryset[:count]
        return queryset


def index(request: WSGIRequest) -> HttpResponse:
    query = Country.objects.language(request.LANGUAGE_CODE).filter(is_published=True).order_by('name').all()
    parts = query.filter(is_global=True)
    countries = query.filter(is_global=False)
    return render(request, 'index.html', {'countries': countries, 'parts': parts})


def infobox(request: WSGIRequest, pk: str) -> HttpResponse:
    obj = Area.objects.get(pk=pk)
    return render(request, 'maps/infobox.html', {'data': obj.infobox})


def infobox_by_id(request: WSGIRequest, pk: str) -> HttpResponse:
    obj = Area.objects.get(pk=pk)
    items = obj.infobox
    name = items.pop('name', None)
    wiki = items.pop('wiki', None)
    flag = items.pop('flag', None)
    coat_of_arms = items.pop('coat_of_arms', None)
    items = [{'title': _(key.title()), 'value': value} for key, value in items.items()]
    return JsonResponse({'name': name, 'wiki': wiki, 'image': flag if flag else coat_of_arms, 'items': items})


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    params = request.GET.copy()
    params['country'] = name
    params['lang'] = request.LANGUAGE_CODE
    form = MapForm(params)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    result = [{
        'id': area.id,
        'name': area.name,
        'polygon': area.polygon_gmap,
        'center': area.center,
        'answer': [list(area.answer.coords[0]), list(area.answer.coords[1])],
        'default_position': area.country.pop_position()}
            for area in form.areas()]
    return JsonResponse(result, safe=False)


def maps(request: WSGIRequest, name: str) -> HttpResponse:
    return render(request, 'maps/map.html', context={'country': Country.objects.get(slug=name)})


def react(request: WSGIRequest) -> HttpResponse:
    return render(request, 'map.html', context={'country': Country.objects.get(slug='italy')})
