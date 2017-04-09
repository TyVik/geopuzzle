import tempfile

from django import forms
from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from hvad.utils import load_translation

from maps.models import Country, Area, DIFFICULTY_LEVELS


class MapForm(forms.Form):
    id = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=False)
    difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVELS, required=False, initial=1)

    def __init__(self, country, lang, *args, **kwargs):
        self.country = get_object_or_404(Country, slug=country)
        self.lang = lang
        super(MapForm, self).__init__(*args, **kwargs)

    def areas(self) -> QuerySet:
        if len(self.cleaned_data['id']) > 0:
            return self.cleaned_data['id']

        queryset = Area.objects.language(self.lang).filter(country=self.country).exclude(difficulty=0).order_by('?')
        if self.cleaned_data['difficulty'] != '':
            queryset = queryset.filter(difficulty=int(self.cleaned_data['difficulty']))
        return queryset


class KMLImportForm(forms.Form):
    def extract_polygon(self, geos):
        return geos if isinstance(geos, MultiPolygon) else MultiPolygon(geos)


class KMLCountryImportForm(KMLImportForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), disabled=True)
    kml = forms.FileField()
    language = forms.CharField()

    def save(self) -> None:
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(self.cleaned_data['kml'].read())
            temp.seek(0)
            source = DataSource(temp.name)
            for layer in source:
                for feat in layer:
                    area = Area.objects.create(name=feat['Name'].value, country=self.cleaned_data["country"],
                                               polygon=self.extract_polygon(feat.geom.geos), difficulty=2)
                    for lang, _ in settings.LANGUAGES:
                        trans = load_translation(area, lang, enforce=True)
                        trans.master = area
                        trans.name = feat['Name'].value
                        trans.save()


class KMLAreaImportForm(KMLImportForm):
    area = forms.ModelChoiceField(queryset=Area.objects.all(), disabled=True)
    kml = forms.FileField()

    def save(self) -> None:
        area = self.cleaned_data['area']
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(self.cleaned_data['kml'].read())
            temp.seek(0)
            source = DataSource(temp.name)
            for layer in source:
                for feat in layer:
                    area.polygon = self.extract_polygon(feat.geom.geos)
                    area.save()
