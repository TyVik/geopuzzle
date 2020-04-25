from typing import Dict, TypedDict

from django.http import JsonResponse
from django.views.generic.list import BaseListView
from sorl.thumbnail import get_thumbnail

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
