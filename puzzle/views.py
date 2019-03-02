from typing import List, Dict, Optional

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.translation import ugettext as _, get_language

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.edit import BaseUpdateView
from django.views.generic.list import BaseListView
from sorl.thumbnail import get_thumbnail

from puzzle.forms import PuzzleForm, PuzzleEditForm
from maps.models import Region, Tag
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


class PuzzleEditView(TemplateResponseMixin, BaseUpdateView):
    model = Puzzle
    queryset = None
    slug_field = 'slug'
    context_object_name = None
    slug_url_kwarg = 'name'
    query_pk_and_slug = False
    template_name = 'puzzle/edit.html'
    form_class = PuzzleEditForm

    def get_object(self, queryset=None):
        if self.kwargs.get(self.slug_url_kwarg) == 'new':
            obj = Puzzle(zoom=4, center=Point(0, 0), user=self.request.user)
        else:
            obj = super(PuzzleEditView, self).get_object(queryset)
            if obj.user != self.request.user:
                raise PermissionDenied
        return obj

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'url': f"{reverse('profile')}#puzzle"})

    def get_context_data(self, **kwargs):
        def build_tree(tree, id_in_tree, regions) -> List[Dict]:

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

                root = find(tree, str(region.parent_id))
                id_in_tree.add(region.id)
                root['toggled'] = True
                root['items'] = insert(root['items'], region.json(self.request.LANGUAGE_CODE))
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
        result['tags'] = Tag.get_all(self.request.LANGUAGE_CODE)
        if self.object.id is None:
            result.update({
                'checked': [],
                'regions': [x.json(self.request.LANGUAGE_CODE) for x in Region.objects.filter(parent__isnull=True, is_enabled=True).all()],
                'fields': {
                    'tags': [],
                    'is_published': False,
                    'translations': [{'code': code, 'language': lang, 'title': ''} for code, lang in settings.LANGUAGES]
                }
            })
        else:
            result['checked'] = [region.full_info(self.request.LANGUAGE_CODE) for region in self.object.regions.all()]
            tree = [x.json(self.request.LANGUAGE_CODE) for x in Region.objects.filter(parent__isnull=True, is_enabled=True).all()]
            tree = sorted(tree, key=lambda x: x['name'])  # IMHO it's cheaper than SQL
            result['regions'] = build_tree(tree, set([int(x['id']) for x in tree]), self.object.regions.all())
            result['fields'] = {
                'tags': [x.id for x in self.object.tags.all()],
                'is_published': self.object.is_published,
                'translations': [{'code': translation.language_code, 'title': translation.name,
                                  'language': next(pair for pair in settings.LANGUAGES if pair[0] == translation.language_code)[1]}
                                 for translation in self.object.translations.all()],
            }
        return result


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


class WorkshopItems(BaseListView):
    model = Puzzle
    paginate_by = 30

    ordering = ('-id',)

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

    def render_to_response(self, context):
        def json(item: Puzzle) -> Dict:
            trans = item.load_translation(get_language())
            return {
                'image': get_thumbnail(item.image.name, geometry_string='196x196', format='PNG', quality='80').url,
                'url': item.get_absolute_url(),
                'name': trans.name,
                'user': item.user.username,
            }

        return JsonResponse([json(x) for x in context['page_obj'].object_list], safe=False)
