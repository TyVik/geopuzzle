from django.conf import settings
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from maps.models import Region
from puzzle.forms import RegionForm
from puzzle.models import Puzzle


def infobox_by_id(request: WSGIRequest, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.strip_infobox)


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    puzzle = get_object_or_404(Puzzle, slug=name)
    form = RegionForm(data=request.GET, puzzle=puzzle, lang=request.LANGUAGE_CODE)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    result = [{
        'id': area.id,
        'name': area.name,
        'polygon': area.polygon_strip,
        'center': area.center,
        'default_position': puzzle.pop_position()}
            for area in form.areas()]
    return JsonResponse(result, safe=False)


def puzzle(request: WSGIRequest, name: str) -> HttpResponse:
    puzzle = get_object_or_404(Puzzle, slug=name)
    context = {
        'google_key': settings.GOOGLE_KEY,
        'language': request.LANGUAGE_CODE,
        'country': puzzle,
        'text': _('{} was assembled! You time is ').format(puzzle.name if puzzle.id != 1 else _('World map'))
    }
    return render(request, 'puzzle/map.html', context=context)
