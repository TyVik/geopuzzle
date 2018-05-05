from typing import List, Dict, Optional

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
        def build_tree(tree, regions) -> List[Dict]:
            id_in_tree = set()

            def attach_node(tree: List[Dict], region: Region) -> List[Dict]:
                def find(tree: List[Dict], id: str) -> Optional[Dict]:
                    for el in tree:
                        if el['id'] == id:
                            return el
                        elif 'items' in el:
                            children = find(el['items'], id)
                            if children is not None:
                                return children
                    return None

                def insert(items, d):
                    index = next((i for i, item in enumerate(items) if item['id'] == d['id']), -1)
                    items[index] = d
                    return items

                id = region.id if region.parent is None else region.parent_id
                root = find(tree, str(id))
                id_in_tree.add(region.id)
                d = region.json
                d['toggled'] = region not in regions
                if region.parent is None:
                    tree = insert(tree, d)
                else:
                    root['items'] = insert(root['items'], d)
                return tree

            def handle_node(tree: List[Dict], region: Region) -> List[Dict]:
                if region.id not in id_in_tree:
                    if (region.parent_id not in id_in_tree) and (region.parent_id is not None):
                        tree = handle_node(tree, region.parent)
                    tree = attach_node(tree, region)
                return tree

            for region in regions:
                tree = handle_node(tree, region)
            return tree

        result = super(PuzzleEditView, self).get_context_data(**kwargs)
        result['checked'] = [{'id': region.id, 'paths': region.polygon_gmap} for region in self.object.regions.all()]
        result['regions'] = build_tree(Region.all_countries(), self.object.regions.all())
        return result
