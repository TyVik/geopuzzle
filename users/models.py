from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import ugettext_lazy as _

from users.fields import CustomAvatarField as AvatarField


class User(AbstractUser):
    image = AvatarField(_('Avatar'), upload_to='avatars', width=100, height=100, null=True)
    language = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES, default='en')
    is_subscribed = models.BooleanField(_('Subscribed on news'))

    @property
    def games(self) -> QuerySet:
        return self.puzzle_set.all()
