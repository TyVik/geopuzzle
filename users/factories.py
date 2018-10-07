from factory import DjangoModelFactory
from factory.fuzzy import FuzzyText

from users.models import User


class UserFactory(DjangoModelFactory):
    username = FuzzyText()

    class Meta:
        model = User
