from dataclasses import asdict

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .constants import Zoom
from .models import Region, Game


def region(request, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.full_info(request.LANGUAGE_CODE))


def index_scroll(request, game: str) -> JsonResponse:
    klass: Game = apps.get_model(game, game.capitalize())
    limit = min(24, int(request.GET.get('limit', 24)))
    exclude = request.GET.get('ids', '')
    exclude = exclude.split(',') if exclude else []
    qs = (klass.index_qs(request.LANGUAGE_CODE)
              .exclude(zoom__in=(Zoom.WORLD, Zoom.LARGE_COUNTRY))
              .exclude(id__in=exclude)
              .order_by('?')[:limit])
    return JsonResponse([asdict(item.index) for item in qs.all()], safe=False)
