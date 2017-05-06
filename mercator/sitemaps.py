from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone

from maps.models import Game
from puzzle.models import Puzzle
from quiz.models import Quiz


class RegionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def location(self, game: Game):
        return game.get_absolute_url()

    def lastmod(self, obj: Game):
        return timezone.now()


class PuzzleSitemap(RegionSitemap):
    def items(self):
        return Puzzle.objects.filter(Q(is_published=True) | Q(slug='world'))


class QuizSitemap(RegionSitemap):
    def items(self):
        return Quiz.objects.filter(Q(is_published=True) | Q(slug='world'))


class WorldSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['index']

    def location(self, object):
        if object == 'index':
            return reverse(object)
