from django import forms


class RegionContainsForm(forms.Form):
    north = forms.FloatField()
    east = forms.FloatField()
    south = forms.FloatField()
    west = forms.FloatField()

    def __init__(self, region, zoom, *args, **kwargs):
        self.region = region
        self.zoom = zoom
        super(RegionContainsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegionContainsForm, self).clean()
        data = {part: cleaned_data[part] for part in ['north', 'south', 'west', 'east']}
        diff = (-1, -1, 1, 1)
        extent = self.region.polygon_bounds
        scale = 1.0 / (self.zoom - 2)
        points = [extent[i] + diff[i] * scale for i in range(4)]
        if not (data['north'] < points[3] and data['south'] > points[1] and
                        data['east'] < points[2] and data['west'] > points[0]):
            raise forms.ValidationError('Point not in polygons')
