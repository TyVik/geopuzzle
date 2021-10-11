from typing import Type, Dict

from django.apps import apps
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic.list import BaseListView

from common.middleware import WSGILanguageRequest
from .constants import Zoom, GAMES
from .models import Region, Game


def region(request, pk: str) -> JsonResponse:
    obj = get_object_or_404(Region, pk=pk)
    return JsonResponse(obj.full_info(request.LANGUAGE_CODE))


def index_scroll(request, game: str) -> JsonResponse:
    klass: Type[Game] = apps.get_model(*GAMES[game])
    limit = min(24, int(request.GET.get('limit', 24)))
    exclude = request.GET.get('ids', '')
    exclude = exclude.split(',') if exclude else []
    qs = (klass.index_qs(request.LANGUAGE_CODE, with_user=True)
          .exclude(zoom__in=(Zoom.WORLD, Zoom.LARGE_COUNTRY))
          .exclude(id__in=exclude)
          .order_by('?')[:limit])
    result = [item.index('196x196') for item in qs.all()]
    return JsonResponse(result, safe=False)


AutocompleteItem = Dict[str, str]


class ScrollListView(BaseListView):
    model = None
    paginate_by = 30
    ordering = ('-id',)

    def render_to_response(self, context, **kwargs) -> JsonResponse:
        return JsonResponse([x.index('196x196') for x in context['page_obj'].object_list], safe=False)


class GameView(View):
    template: str

    @classmethod
    def _google_key(cls, request: WSGILanguageRequest) -> str:
        return '' if settings.DISABLE_GOOGLE_KEY else settings.GOOGLE_KEY

    def get(self, request: WSGILanguageRequest, name: str, *args, **kwargs) -> HttpResponse:
        obj = get_object_or_404(self.model, slug=name)
        context = {
            'game': obj,
            'game_data': obj.get_game_data(request.LANGUAGE_CODE),
            'gmap_key': self._google_key(request),
        }
        return render(request, self.template, context=context)


class QuestionView(View):
    model: Game

    @never_cache  # for HTTP headers
    def get(self, request: WSGILanguageRequest, name: str, *args, **kwargs) -> JsonResponse:
        request._cache_update_cache = False  # disable internal cache pylint: disable=protected-access
        obj = get_object_or_404(self.model, slug=name)
        form = self.form(data=request.GET, game=obj)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        return JsonResponse(form.json())
