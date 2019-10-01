from typing import Dict

from django.utils.translation import get_language
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from sorl.thumbnail import get_thumbnail

from maps.models import Game


class ScrollListView(BaseListView):
    model = None
    paginate_by = 30
    ordering = ('-id',)

    @classmethod
    def item_to_json(cls, item: Game) -> Dict:
        trans = item.load_translation(get_language())
        return {
            'image': get_thumbnail(item.image.name, geometry_string='196x196', format='JPEG', quality=66).url,
            'url': item.get_absolute_url(),
            'name': trans.name,
            'user': item.user.username,
        }

    def render_to_response(self, context):
        return JsonResponse([self.item_to_json(x) for x in context['page_obj'].object_list], safe=False)
