from django.utils.translation import ugettext as _

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from common.middleware import WSGILanguageRequest
from .forms import PuzzleForm
from .models import Puzzle


@never_cache  # for HTTP headers
def questions(request: WSGILanguageRequest, name: str) -> JsonResponse:
    request._cache_update_cache = False  # disable internal cache pylint: disable=protected-access
    obj = get_object_or_404(Puzzle, slug=name)
    form = PuzzleForm(data=request.GET, game=obj)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    return JsonResponse(form.json())


def puzzle(request: WSGILanguageRequest, name: str) -> HttpResponse:
    obj = get_object_or_404(Puzzle, slug=name)
    trans = obj.load_translation(request.LANGUAGE_CODE)
    name = trans.name if obj.pk != 1 else _('World map')
    context = {
        'game': obj,
        'name': trans.name,
        'text': _("""Puzzle \"{}\" has been assembled! Your time is """).format(name)
    }
    return render(request, 'puzzle/map.html', context=context)
