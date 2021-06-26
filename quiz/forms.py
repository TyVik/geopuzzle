from typing import List

from django import forms
from django.db import connection

from common.constants import GameQuestions
from common.utils import get_language
from maps.forms import RegionForm
from quiz.models import Quiz


class PointContainsForm(forms.Form):
    lat = forms.FloatField()
    lng = forms.FloatField()

    CONTAINS_SQL = """SELECT ST_Covers(polygon, p)
FROM (SELECT polygon from maps_region where id = {id}) As polygon, 
    ST_Point({lon}, {lat}) as p;"""

    def __init__(self, area, *args, **kwargs):
        self.area = area
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        with connection.cursor() as cursor:
            cursor.execute(self.CONTAINS_SQL.format(id=self.area.pk, lat=cleaned_data.get('lat'),
                                                    lon=cleaned_data.get('lng')))  # lgtm [py/sql-injection]
            row = cursor.fetchone()
            result = row[0]
        if not result:
            raise forms.ValidationError('Point not in polygons')


class QuizInfoboxForm(RegionForm):
    params = forms.CharField()

    game: Quiz

    def clean_params(self) -> List[str]:
        return self.cleaned_data['params'].split(',')

    def json(self) -> GameQuestions:
        def extract_capital(capital) -> str:
            return capital['name'] if isinstance(capital, dict) else capital

        should_be_solved = [x.region_id for x in self.game.quizregion_set.all() if x.is_solved]
        questions = []
        solved = []
        for region in self.regions:
            trans = region.translation
            if trans.infobox is None or region.pk in should_be_solved:
                solved.append(region.full_info(get_language()))
                continue
            k = {}
            for param in self.cleaned_data['params']:
                if param == 'capital':
                    capital = trans.infobox.get('capital', None)
                    value = trans.infobox.get('name', None) if capital is None else extract_capital(capital)
                elif param == 'name':
                    value = trans.infobox.get('name', None)
                else:
                    value = trans.infobox.get(param, None)
                if value is not None:
                    k[param] = value

            # if question has not values - set them as founded
            if k != {}:
                k['id'] = region.pk
                k['name'] = trans.infobox.get('name', None)
                questions.append(k)
            else:
                solved.append(region.full_info(get_language()))
        return GameQuestions(questions=questions, solved=solved)
