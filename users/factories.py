import string

from factory import DjangoModelFactory
from factory.fuzzy import FuzzyText

from .models import User


class UserFactory(DjangoModelFactory):
    username = FuzzyText(chars=string.ascii_lowercase)
    email = FuzzyText(suffix='@email.org', chars=string.ascii_lowercase)

    class Meta:
        model = User
