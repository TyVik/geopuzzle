import tempfile

from django import forms
from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Point
from hvad.utils import load_translation

from maps.models import Country, Area


class AreaContainsForm(forms.Form):
    north = forms.FloatField()
    east = forms.FloatField()
    south = forms.FloatField()
    west = forms.FloatField()

    def __init__(self, area, *args, **kwargs):
        self.area = area
        super(AreaContainsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AreaContainsForm, self).clean()
        data = {part: cleaned_data[part] for part in ['north', 'south', 'west', 'east']}
        points = self.area.polygon_bounds
        if not (data['north'] < points[3] and data['south'] > points[1] and
                        data['east'] < points[2] and data['west'] > points[0]):
            raise forms.ValidationError('Point not in polygons')


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
