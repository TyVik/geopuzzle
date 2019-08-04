from django.conf import settings
from django.db import connection
from django.http import JsonResponse

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from redis import StrictRedis

from maps.models import Region
from puzzle.models import Puzzle
from quiz.models import Quiz


def index(request: WSGIRequest) -> HttpResponse:
    games = []
    for game in (Puzzle, Quiz):
        name = game.__name__.lower()
        qs = game.objects.\
            filter(translations__language_code=request.LANGUAGE_CODE, is_published=True, on_main_page=True).\
            prefetch_related('translations').\
            order_by('translations__name')
        games.append({
            'items': {
                'parts': [item.index for item in qs.all() if item.is_global],
                'countries': [item.index for item in qs.all() if not item.is_global]
            },
            'name': name,
            'link': f'{name}_map',
            'caption': game.name(),
            'rules': game.description()
        })
    return render(request, 'index.html', {'games': games})


def infobox_by_id(request: WSGIRequest, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.polygon_infobox[request.LANGUAGE_CODE])


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
