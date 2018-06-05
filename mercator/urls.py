"""mercator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView


from mercator import views
from .sitemaps import WorldSitemap, PuzzleSitemap, QuizSitemap


sitemaps = {
    'world': WorldSitemap,
    'puzzle': PuzzleSitemap,
    'quiz': QuizSitemap,
}


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('users.urls')),
    url(r'^puzzle/', include('puzzle.urls')),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^regions/', include('maps.urls')),
    url(r'^maps/(?P<name>[a-zA-Z0-9]+)/', views.deprecated_redirect),
    url(r'^puzzle/area/(?P<pk>\d+)/infobox/', views.infobox_by_id, name='infobox_by_id'),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt'), name='robots'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    url(r'^error/$', views.error, name='error'),
    url(r'^status/$', views.status, name='status'),
    url(r'^$', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)