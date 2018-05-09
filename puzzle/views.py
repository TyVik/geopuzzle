import base64
import string
from random import uniform
from typing import List, Dict, Optional

from django.conf import settings
from django.contrib.gis.geos import Point, MultiPoint
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.base import ContentFile
from django.forms import ModelForm, Field
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import BaseUpdateView

from puzzle.forms import PuzzleForm
from maps.models import Region
from puzzle.models import Puzzle, PuzzleRegion, PuzzleTranslation


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


class BoundsField(Field):
    default_error_messages = {
        'invalid': 'Enter comma separated numbers only.',
    }

    def to_python(self, value):
        try:
            value = [float(item.strip()) for item in value.split(',') if item.strip()]
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'])
        return value


class PuzzleEditForm(ModelForm):
    bounds = BoundsField()

    class Meta:
        model = Puzzle
        fields = ('regions', 'image', 'center', 'zoom', 'is_published')

    def clean_image(self):
        format, imgstr = self.data.get('image').split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

    def save(self, *args, **kwargs):
        def get_slug(slug: str) -> str:
            return get_random_string(15, string.ascii_lowercase + string.digits) \
                if slug == '' else slug

        def get_positions(bounds: List[float], count: int) -> List:
            return [Point(uniform(bounds[0], bounds[2]), uniform(bounds[1], bounds[3]))
                    for _ in range(round(count * 2 / 3) + 1)]

        self.instance.slug = get_slug(self.instance.slug)
        self.instance.default_positions = MultiPoint(get_positions(
            self.cleaned_data['bounds'], len(self.cleaned_data['regions'])))
        return super(PuzzleEditForm, self).save(*args, **kwargs)

    def _save_m2m(self):
        PuzzleRegion.objects.filter(puzzle=self.instance).delete()
        PuzzleRegion.objects.bulk_create([
            PuzzleRegion(puzzle=self.instance, region=region)
            for region in self.cleaned_data['regions']])

        for lang in settings.ALLOWED_LANGUAGES:
            PuzzleTranslation.objects.update_or_create(
                master=self.instance, language_code=lang,
                defaults={'name': self.data.get(f'{lang}_name', '')})


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
                root['items'] = insert(root['items'], region.json)
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
        if self.object.id is None:
            result.update({
                'checked': [],
                'regions': [x.json for x in Region.objects.filter(parent__isnull=True).all()],
                'fields': {
                    'is_published': False,
                    'translations': [{'code': code, 'language': lang, 'title': ''} for code, lang in settings.LANGUAGES]
                }
            })
        else:
            result['checked'] = [region.full_info(self.request.user.language) for region in self.object.regions.all()]
            tree = [x.json for x in Region.objects.filter(parent__isnull=True).all()]
            result['regions'] = build_tree(tree, set([int(x['id']) for x in tree]), self.object.regions.all())
            result['fields'] = {
                'is_published': self.object.is_published,
                'translations': [{'code': translation.language_code, 'title': translation.name,
                                  'language': next(pair for pair in settings.LANGUAGES if pair[0] == translation.language_code)[1]}
                                 for translation in self.object.translations.all()],
            }
        return result


class WorkshopView(ListView):
    model = Puzzle
    template_name = 'puzzle/list.html'
    ordering = '-created'

    def get_queryset(self):
        return super(WorkshopView, self).get_queryset().filter(user__isnull=False, is_published=True)
