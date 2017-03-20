from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from maps.models import Country


def index(request: WSGIRequest) -> HttpResponse:
    query = Country.objects.language(request.LANGUAGE_CODE).filter(is_published=True).order_by('name').all()
    parts = query.filter(is_global=True)
    countries = query.filter(is_global=False)
    games = {
        'puzzle': {
            'link': 'puzzle_map',
            'caption': _('puzzle'),
            'rules': _('Drag the shapes of countries on the right place.')
        },
        'quiz': {
            'link': 'quiz_map',
            'caption': _('quiz'),
            'rules': _('Find all countries or regions by their attributes: name, flag, emblem or capital.')
        }
    }
    return render(request, 'index.html', {'countries': countries, 'parts': parts, 'games': games})
