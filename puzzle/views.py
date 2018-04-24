from django.conf import settings
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseUpdateView

from puzzle.forms import PuzzleForm
from maps.models import Region
from puzzle.models import Puzzle


@never_cache  # for HTTP headers
def questions(request: WSGIRequest, name: str) -> JsonResponse:
    request._cache_update_cache = False  # disable internal cache
    puzzle = get_object_or_404(Puzzle, slug=name)
    form = PuzzleForm(data=request.GET, game=puzzle)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    return JsonResponse(form.json())


def puzzle(request: WSGIRequest, name: str) -> HttpResponse:
    puzzle = get_object_or_404(Puzzle, slug=name)
    trans = puzzle.load_translation(request.LANGUAGE_CODE)
    context = {
        'google_key': settings.GOOGLE_KEY,
        'language': request.LANGUAGE_CODE,
        'game': puzzle,
        'name': trans.name,
        'text': _('{} was assembled! You time is ').format(trans.name if puzzle.id != 1 else _('World map'))
    }
    return render(request, 'puzzle/map.html', context=context)


class PuzzleEditView(TemplateResponseMixin, BaseUpdateView):
    model = Puzzle
    fields = ['slug']
    queryset = None
    slug_field = 'slug'
    context_object_name = None
    slug_url_kwarg = 'name'
    query_pk_and_slug = False
    template_name = 'puzzle/edit.html'

    def get_context_data(self, **kwargs):
        result = super(PuzzleEditView, self).get_context_data(**kwargs)
        result['checked'] = list(map(str, self.object.regions.values_list('id', flat=True)))
        result['regions'] = [region.tree for region in Region.objects.filter(parent_id=6993).all()]
        return result
