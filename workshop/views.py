from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import TemplateView
from django.utils.translation import get_language
from django.views.generic.list import BaseListView

from common.views import ScrollListView
from maps.models import Tag
from puzzle.models import Puzzle
from workshop.filters import WorkshopFilter, TagFilter, ORDER


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
            filter(user__isnull=False, is_published=True,
                   translations__language_code=self.request.LANGUAGE_CODE).\
            prefetch_related('translations')
        return WorkshopFilter(self.request.GET, qs).qs.distinct()


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
