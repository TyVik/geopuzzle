from factory import SubFactory
from factory.django import DjangoModelFactory

from maps.factories import GameFactory, RegionFactory
from .models import Quiz, QuizRegion


class QuizFactory(GameFactory):
    class Meta:
        model = Quiz


class QuizRegionFactory(DjangoModelFactory):
    region = SubFactory(RegionFactory)
    quiz = SubFactory(QuizFactory)
    is_solved = False

    class Meta:
        model = QuizRegion
