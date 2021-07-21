from __future__ import annotations

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import ugettext as _

from django_enumfield import enum

from common.constants import Point, LanguageEnumType
from common.utils import get_language
from ..constants import Zoom, IndexPageGame, IndexPageGameType, InitGameParams, InitGameMapOptions, GameData


class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='games', blank=True, null=True)
    slug = models.CharField(max_length=15, db_index=True, unique=True)
    center = PointField(geography=True)
    zoom = enum.EnumField(Zoom, default=Zoom.COUNTRY)
    is_published = models.BooleanField(default=False, db_index=True)
    is_global = models.BooleanField(default=False)
    on_main_page = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    translations: QuerySet[GameTranslation]

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return reverse(f'{self.__class__._meta.model_name}_map', args=(self.slug,))

    def load_translation(self, lang: LanguageEnumType) -> GameTranslation:
        for translation in self.translations.all():
            if translation.language_code == lang:
                return translation
        return self.translations.all()[0]

    @classmethod
    def reverse_link(cls) -> str:
        return f'{cls._meta.model_name}_map'

    @property
    def index(self) -> IndexPageGame:
        trans = self.load_translation(get_language())
        return IndexPageGame(image=self.image.name, slug=self.slug, name=trans.name, id=self.pk)

    @classmethod
    def index_qs(cls, language: LanguageEnumType) -> QuerySet:
        return cls.objects.\
            filter(translations__language_code=language, is_published=True, on_main_page=True).\
            prefetch_related('translations').\
            order_by('translations__name')

    @classmethod
    def index_items(cls, language: LanguageEnumType) -> IndexPageGameType:
        qs = cls.index_qs(language).filter(zoom__in=(Zoom.WORLD, Zoom.LARGE_COUNTRY))
        return IndexPageGameType(
            world=[item.index for item in qs.all() if item.zoom == Zoom.WORLD],
            parts=[item.index for item in qs.all() if item.zoom == Zoom.LARGE_COUNTRY],
        )

    @classmethod
    def name(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def description(cls) -> str:
        raise NotImplementedError()

    def parts(self) -> str:
        return _('countries') if self.is_global else _('regions')

    def get_game_data(self, language: LanguageEnumType) -> GameData:
        trans = self.load_translation(language)
        return GameData(
            name=trans.name if self.pk != 1 else _('World map'),
            parts=self.parts()
        )

    def get_init_params(self) -> InitGameParams:
        return InitGameParams(
            zoom=self.zoom,
            center=Point(lat=self.center.coords[1], lng=self.center.coords[0]),
            options=InitGameMapOptions(streetViewControl=False, mapTypeControl=False)
        )


class GameTranslation(models.Model):
    name = models.CharField(max_length=50)
    language_code = models.CharField(max_length=2, choices=settings.LANGUAGES, db_index=True)
    master = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='translations', editable=False)

    class Meta:
        unique_together = ('language_code', 'master')
        abstract = True
