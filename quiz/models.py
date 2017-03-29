from django.db import models

from maps.models import Country


class Option(models.Model):
    name = models.CharField(max_length=20)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.name