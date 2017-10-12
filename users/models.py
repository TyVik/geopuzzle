from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.URLField(null=True)
    language = models.CharField(max_length=2, default='en', choices=settings.LANGUAGES)
