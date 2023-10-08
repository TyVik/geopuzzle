from typing import Iterable

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone

from maps.models import Game
from puzzle.models import Puzzle
from quiz.models import Quiz


class RegionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def location(self, item: Game) -> str:
        return item.get_absolute_url()

    def lastmod(self, _):
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

    def items(self) -> Iterable[str]:
        return 'index', 'workshop'

    def location(self, item: str) -> str:
        return reverse(item)
