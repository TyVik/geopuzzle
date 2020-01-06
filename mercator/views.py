from django.conf import settings
from django.db import connection
from django.http import JsonResponse

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from redis import StrictRedis

from common.middleware import WSGILanguageRequest
from maps.models import Region
from puzzle.models import Puzzle
from quiz.models import Quiz


def index(request: WSGILanguageRequest) -> HttpResponse:
    games = []
    for game in (Puzzle, Quiz):
        name = game.__name__.lower()
        games.append({
            'items': game.index_items(request.LANGUAGE_CODE),
            'name': name,
            'link': game.reverse_link(),
            'caption': game.name(),
            'rules': game.description()
        })
    return render(request, 'index.html', {'games': games, 'gmap_limit': not settings.GOOGLE_KEY})


def infobox_by_id(request: WSGILanguageRequest, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.polygon_infobox[request.LANGUAGE_CODE])


def error(request: WSGIRequest) -> HttpResponse:
    return HttpResponse('Something went wrong :(')


def status(request: WSGIRequest) -> JsonResponse:
    def check_redis() -> None:
        StrictRedis.from_url(f'redis://{settings.REDIS_HOST}:6379/0').ping()

    def check_database() -> None:
        connection.cursor()

    result = {}
    for service in ('redis', 'database'):
        try:
            locals()[f'check_{service}']()
            result[service] = 'success'
        except Exception as e:
            return JsonResponse({service: 'fail', 'message': str(e)}, status=503)
    return JsonResponse(result)
