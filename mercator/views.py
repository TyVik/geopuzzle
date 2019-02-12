from django.conf import settings
from django.db import connection
from django.http import HttpResponsePermanentRedirect, JsonResponse
from django.urls import reverse
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from redis import StrictRedis

from maps.models import Region
from puzzle.models import Puzzle
from quiz.models import Quiz


def index(request: WSGIRequest) -> HttpResponse:
    puzzles = Puzzle.objects.filter(translations__language_code=request.LANGUAGE_CODE, is_published=True, on_main_page=True).order_by('translations__name').all()
    quizzes = Quiz.objects.filter(translations__language_code=request.LANGUAGE_CODE, is_published=True, on_main_page=True).order_by('translations__name').all()
    games = [{
        'items': {
            'parts': [item.index for item in puzzles.filter(is_global=True).all()],
            'countries': [item.index for item in puzzles.filter(is_global=False).all()]
        },
        'name': 'puzzle',
        'link': 'puzzle_map',
        'caption': _('puzzle'),
        'rules': _('In the Puzzle you need to drag the shape of the territory to the right place. Just like in childhood we collected pictures piece by piece, so here you can collect a country from regions or whole continents from countries!')
    }, {
        'items': {
            'parts': [item.index for item in quizzes.filter(is_global=True).all()],
            'countries': [item.index for item in quizzes.filter(is_global=False).all()]
        },
        'name': 'quiz',
        'link': 'quiz_map',
        'caption': _('quiz'),
        'rules': _('In the Quiz you need find the country by flag, emblem or the capital. Did you know that Monaco and Indonesia have the same flags? And that the flags of the United States and Liberia differ only in the number of stars? So, these and other interesting things can be learned and remembered after brainstorming right now!')
    }]
    return render(request, 'index.html', {'games': games})


def infobox_by_id(request: WSGIRequest, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.polygon_infobox[request.LANGUAGE_CODE])


def deprecated_redirect(request: WSGIRequest, name: str) -> HttpResponsePermanentRedirect:
    return HttpResponsePermanentRedirect(reverse('puzzle_map', kwargs={'name': name}))


def error(request) -> HttpResponse:
    return HttpResponse('Something went wrong :(')


def status(request) -> JsonResponse:
    def check_redis():
        StrictRedis.from_url(f'redis://{settings.REDIS_HOST}:6379/0').ping()

    def check_database():
        connection.cursor()

    result = {}
    for service in ('redis', 'database'):
        try:
            locals()[f'check_{service}']()
            result[service] = 'success'
        except Exception as e:
            return JsonResponse({service: 'fail', 'message': str(e)}, status=503)
    return JsonResponse(result)
