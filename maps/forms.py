import tempfile

from django import forms
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon

from maps.models import Country, Area


class KMLImportForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), disabled=True)
    kml = forms.FileField()

    def save(self):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(self.cleaned_data['kml'].read())
            temp.seek(0)
            source = DataSource(temp.name)
            for layer in source:
                for feat in layer:
                    polygon = feat.geom.geos if isinstance(feat.geom.geos, MultiPolygon) else MultiPolygon(feat.geom.geos)
                    area = Area.objects.create(name=feat['Name'].value, country=self.cleaned_data["country"], polygon=polygon)
                    area.recalc_answer()
