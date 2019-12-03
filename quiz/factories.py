import factory
from factory import SubFactory
from factory.django import DjangoModelFactory

from maps.factories import GameFactory, RegionFactory
from .models import Quiz, QuizRegion


class QuizFactory(GameFactory):
    class Meta:
        model = Quiz

    @factory.post_generation
    def translations(self, create, extracted, **kwargs):
        for translation in self.translations.all():
            translation.name = f'{translation.name}-{translation.language_code}'
            translation.save()


class QuizRegionFactory(DjangoModelFactory):
    region = SubFactory(RegionFactory)
    quiz = SubFactory(QuizFactory)
    is_solved = False

    class Meta:
        model = QuizRegion
