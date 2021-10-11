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
    games = [{
        'items': game.index_items(request.LANGUAGE_CODE),
        'name': game.category,
        'link': game.reverse_link(),
        'caption': game.name(),
    } for game in (Puzzle, Quiz)]
    google_key = settings.GOOGLE_KEY \
        if not settings.DISABLE_GOOGLE_KEY or request.user.has_perm('puzzle.patron') else ''
    return render(request, 'index.html', {'games': games, 'gmap_key': google_key})


def infobox_by_id(request: WSGILanguageRequest, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.polygon_infobox[request.LANGUAGE_CODE])


def error(request: WSGIRequest) -> HttpResponse:
    return HttpResponse('Something went wrong :(')


def status(request: WSGIRequest) -> JsonResponse:
    def check_redis() -> None:  # pylint: disable=possibly-unused-variable
        StrictRedis.from_url(f'redis://{settings.REDIS_HOST}:6379/0').ping()

    def check_database() -> None:  # pylint: disable=possibly-unused-variable
        connection.cursor()

    result = {}
    for service in ('redis', 'database'):
        try:
            locals()[f'check_{service}']()
            result[service] = 'success'
        except Exception:  # pylint: disable=broad-except
            return JsonResponse({service: 'fail'}, status=503)
    return JsonResponse(result)
