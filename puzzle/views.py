from typing import Dict

from django.utils.translation import ugettext as _, get_language

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView
from django.views.generic.list import BaseListView
from sorl.thumbnail import get_thumbnail

from puzzle.forms import PuzzleForm
from maps.models import Tag
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
        'game': puzzle,
        'name': trans.name,
        'text': _('Puzzle \"{}\" has been assembled! Your time is ').format(trans.name if puzzle.id != 1 else _('World map'))
    }
    return render(request, 'puzzle/map.html', context=context)


class ScrollListView(BaseListView):
    model = Puzzle
    paginate_by = 30
    ordering = ('-id',)

    @classmethod
    def item_to_json(cls, item: Puzzle) -> Dict:
        trans = item.load_translation(get_language())
        return {
            'image': get_thumbnail(item.image.name, geometry_string='196x196', format='PNG', quality='80').url,
            'url': item.get_absolute_url(),
            'name': trans.name,
            'user': item.user.username,
        }

    def render_to_response(self, context):
        return JsonResponse([self.item_to_json(x) for x in context['page_obj'].object_list], safe=False)


class WorkshopView(TemplateView):
    template_name = 'puzzle/list.html'

    def get_context_data(self, **kwargs):
        context = super(WorkshopView, self).get_context_data(**kwargs)
        context.update({
            'count': Puzzle.objects.get_queryset().filter(user__isnull=False, is_published=True).count(),
            'language': get_language(),
            'tags': Tag.get_all(self.request.LANGUAGE_CODE),
        })
        return context


class WorkshopItems(ScrollListView):
    def get_queryset(self):
        qs = super(WorkshopItems, self).get_queryset()
        qs = qs.filter(user__isnull=False, is_published=True).prefetch_related('translations')

        search = self.request.GET.get('search', None)
        if search:
            qs = qs.filter(translations__name__icontains=search)

        tag = self.request.GET.get('tag', None)
        if tag:
            qs = qs.filter(tags=tag)
        return qs
