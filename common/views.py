from typing import Dict, TypedDict

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic.list import BaseListView
from sorl.thumbnail import get_thumbnail

from common.middleware import WSGILanguageRequest
from common.utils import get_language
from maps.models import Game


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
        trans = obj.load_translation(request.LANGUAGE_CODE)
        context = {
            'game': obj,
            'name': trans.name,
            'text': obj.congratulation_text(request.LANGUAGE_CODE),
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
