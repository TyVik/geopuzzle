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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from common.constants import DAY, HOUR, MINUTE
from mercator import views
from .sitemaps import WorldSitemap, PuzzleSitemap, QuizSitemap


sitemaps = {
    'world': WorldSitemap,
    'puzzle': PuzzleSitemap,
    'quiz': QuizSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls', namespace='accounts')),
    path('puzzle/', include('puzzle.urls', namespace='puzzle')),
    path('quiz/', include('quiz.urls', namespace = 'quiz')),
    path('', include('maps.urls')),
    path('workshop/', include('workshop.urls', namespace='workshop')),
    path('puzzle/area/<int:pk>/infobox/', cache_page(DAY)(views.infobox_by_id), name='infobox_by_id'),

    path('robots.txt', cache_page(DAY)(TemplateView.as_view(template_name='robots.txt')), name='robots'),
    path('sitemap.xml', cache_page(HOUR)(sitemap), {'sitemaps': sitemaps}, name='sitemap'),

    path('error/', cache_page(DAY)(views.error), name='error'),
    path('status/', cache_page(MINUTE)(views.status), name='status'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
