from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import TemplateView
from django.utils.translation import get_language
from django.views.generic.list import BaseListView

from common.views import ScrollListView
from maps.models import Tag
from puzzle.models import Puzzle
from users.models import User
from workshop.filters import WorkshopFilter, TagFilter, ORDER

SUGGESTION = {
    'author': {'model': User, 'field': 'username'},
    'tag': {'model': Tag, 'field': 'name'}
}


class WorkshopView(TemplateView):
    template_name = 'puzzle/list.html'

    def get_context_data(self, **kwargs):
        context = super(WorkshopView, self).get_context_data(**kwargs)
        context.update({
            'count': Puzzle.objects.get_queryset().filter(user__isnull=False, is_published=True).count(),
            'language': get_language(),
            'order': [(key, value['title']) for key, value in ORDER.items()],
        })
        return context


class WorkshopItems(ScrollListView):
    model = Puzzle

    def get_queryset(self):
        qs = super(WorkshopItems, self).get_queryset().\
            filter(user__isnull=False, is_published=True).\
            prefetch_related('translations')
        return WorkshopFilter(self.request.GET, qs).qs


class TagView(BaseListView):
    model = Tag

    def get_queryset(self):
        return TagFilter(self.request.GET, super(TagView, self).get_queryset()).qs

    @staticmethod
    def convert_item(item):
        return {'value': str(item.id), 'label': item.name}

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse([self.convert_item(item) for item in context['object_list']], safe=False)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseBadRequest(status=401)

        instance, _ = Tag.objects.get_or_create(name=request.POST['name'][:50])
        return JsonResponse(self.convert_item(instance))


def suggest(request):
    for key in request.GET:
        value = request.GET.get(key)
        if value is not None:
            params = SUGGESTION[key]
            qs = params['model'].objects.filter(**{f'{params["field"]}__icontains': value}).values_list('id', params['field'])
            result = [{'value': str(item[0]), 'label': item[1]} for item in qs]
            return JsonResponse(result, safe=False)
    else:
        return HttpResponseBadRequest()
