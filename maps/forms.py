from __future__ import annotations

from django import forms
from django.db.models import QuerySet

from .models import Region, Game


class RegionForm(forms.Form):
    id = forms.ModelMultipleChoiceField(queryset=Region.objects.all(), required=False)

    def __init__(self, game: Game, *args, **kwargs):
        self.game = game
        super().__init__(*args, **kwargs)

    @property
    def regions(self) -> QuerySet[Region]:
        if len(self.cleaned_data['id']) > 0:
            return self.cleaned_data['id']
        return self.game.regions.order_by('?')
