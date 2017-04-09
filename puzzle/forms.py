from django import forms


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
