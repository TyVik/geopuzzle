from django.conf import settings
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from maps.forms import RegionForm
from puzzle.models import Puzzle


def questions(request: WSGIRequest, name: str) -> JsonResponse:
    puzzle = get_object_or_404(Puzzle, slug=name)
    form = RegionForm(data=request.GET, game=puzzle)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    result = [{
        'id': region.id,
        'name': region.translation.name,
        'polygon': region.polygon_strip,
        'center': region.polygon_center,
        'default_position': puzzle.pop_position()}
            for region in form.regions]
    return JsonResponse(result, safe=False)


def puzzle(request: WSGIRequest, name: str) -> HttpResponse:
    puzzle = get_object_or_404(Puzzle, slug=name)
    trans = puzzle.load_translation(request.LANGUAGE_CODE)
    context = {
        'google_key': settings.GOOGLE_KEY,
        'language': request.LANGUAGE_CODE,
        'game': puzzle,
        'text': _('{} was assembled! You time is ').format(trans.name if puzzle.id != 1 else _('World map'))
    }
    return render(request, 'puzzle/map.html', context=context)
