import string
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from maps.models import Tag


class TagFactory(DjangoModelFactory):
    name = FuzzyText(chars=string.ascii_lowercase)

    class Meta:
        model = Tag
