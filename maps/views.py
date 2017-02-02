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
    countries = Country.objects.language(request.LANGUAGE_CODE).filter(is_published=True).exclude(slug='world').order_by('name').all()
    parts = Country.objects.filter(pk__in=[5, 6, 7, 9])
    return render(request, 'index.html', {'countries': countries, 'parts': parts})


def infobox(request: WSGIRequest, pk: str) -> HttpResponse:
    obj = Area.objects.get(pk=pk)
    return render(request, 'maps/infobox.html', {'data': obj.infobox})


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    params = request.GET.copy()
    params['country'] = name
    params['lang'] = request.LANGUAGE_CODE
    form = MapForm(params)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    areas = form.areas()
    return JsonResponse([{
        'id': country.id,
        'name': country.name,
        'polygon': country.polygon_gmap,
        'answer': [list(country.answer.coords[0]), list(country.answer.coords[1])]}
            for country in areas], safe=False)


def maps(request: WSGIRequest, name: str) -> HttpResponse:
    return render(request, 'maps/map.html', context={'country': Country.objects.get(slug=name)})
