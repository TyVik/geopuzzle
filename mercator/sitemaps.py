from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.utils import timezone

from maps.models import Country


class RegionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Country.objects.filter(is_published=True)

    def lastmod(self, country):
        return timezone.now()

    def location(self, country):
        return country.get_absolute_url()


class WorldSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return 'index', 'world', 'america', 'europe', 'africa'

    def location(self, object):
        if object == 'index':
            return reverse(object)
        country = Country.objects.get(slug=object)
        return country.get_absolute_url()