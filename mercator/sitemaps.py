from typing import List, Iterable

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.db.models import Q, QuerySet
from django.utils import timezone

from maps.models import Game
from puzzle.models import Puzzle
from quiz.models import Quiz


class RegionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def location(self, game: Game) -> str:
        return game.get_absolute_url()

    def lastmod(self, obj: Game):
        return timezone.now()


class PuzzleSitemap(RegionSitemap):
    def items(self) -> Iterable[Puzzle]:
        return Puzzle.objects.filter(Q(is_published=True) | Q(slug='world')).order_by('id')


class QuizSitemap(RegionSitemap):
    def items(self) -> Iterable[Quiz]:
        return Quiz.objects.filter(Q(is_published=True) | Q(slug='world')).order_by('id')


class WorldSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self) -> List[str]:
        return ['index']

    def location(self, object: str) -> str:
        if object == 'index':
            return reverse(object)
