from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    image = models.ImageField(_('Avatar'), upload_to='avatars', null=True, max_length=200)
    language = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES, default='en')
    is_subscribed = models.BooleanField(_('Subscribed on news'), default=True)
