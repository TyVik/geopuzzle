from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.fields import CustomAvatarField as AvatarField


class User(AbstractUser):
    image = AvatarField(upload_to='avatars', width=100, height=100, null=True)
    language = models.CharField(_('Language'), max_length=2, choices=settings.LANGUAGES, null=True)
