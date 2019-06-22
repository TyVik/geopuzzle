from factory import DjangoModelFactory
from factory.fuzzy import FuzzyText

from maps.models import Tag


class TagFactory(DjangoModelFactory):
    name = FuzzyText()

    class Meta:
        model = Tag
