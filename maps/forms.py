from django import forms
from django.db.models import QuerySet

from maps.models import Region


class RegionForm(forms.Form):
    id = forms.ModelMultipleChoiceField(queryset=Region.objects.all(), required=False)

    def __init__(self, game, *args, **kwargs):
        self.game = game
        super(RegionForm, self).__init__(*args, **kwargs)

    @property
    def regions(self) -> QuerySet:
        if len(self.cleaned_data['id']) > 0:
            return self.cleaned_data['id']
        return self.game.regions.order_by('?')
