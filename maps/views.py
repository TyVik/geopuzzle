from dataclasses import asdict
from typing import Type, TypedDict, Dict

from django.apps import apps
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic.list import BaseListView
from sorl.thumbnail import get_thumbnail

from common.middleware import WSGILanguageRequest
from common.utils import get_language
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
    qs = (klass.index_qs(request.LANGUAGE_CODE)
          .exclude(zoom__in=(Zoom.WORLD, Zoom.LARGE_COUNTRY))
          .exclude(id__in=exclude)
          .order_by('?')[:limit])
    result = [item.index for item in qs.all()]
    for item in result:
        item.image = get_thumbnail(item.image, '196x196', format='JPEG', quality=70).url
    return JsonResponse([asdict(item) for item in result], safe=False)


AutocompleteItem = Dict[str, str]


class ScrollListItem(TypedDict):
    image: str
    url: str
    name: str
    user: str


class ScrollListView(BaseListView):
    model = None
    paginate_by = 30
    ordering = ('-id',)

    @classmethod
    def item_to_json(cls, item: Game) -> ScrollListItem:
        trans = item.load_translation(get_language())
        return ScrollListItem(
            image=get_thumbnail(item.image.name, geometry_string='196x196', format='JPEG', quality=66).url,
            url=item.get_absolute_url(),
            name=trans.name,
            user=item.user.username if item.user else '',
        )

    def render_to_response(self, context, **kwargs) -> JsonResponse:
        return JsonResponse([self.item_to_json(x) for x in context['page_obj'].object_list], safe=False)


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
    @never_cache  # for HTTP headers
    def get(self, request: WSGILanguageRequest, name: str, *args, **kwargs) -> JsonResponse:
        request._cache_update_cache = False  # disable internal cache pylint: disable=protected-access
        obj = get_object_or_404(self.model, slug=name)
        form = self.form(data=request.GET, game=obj)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        return JsonResponse(form.json())
