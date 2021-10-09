from __future__ import annotations

from typing import Union

from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import TemplateView
from django.views.generic.list import BaseListView

from common.middleware import WSGILanguageRequest
from common.utils import get_language
from maps.models import Tag
from maps.views import ScrollListView, AutocompleteItem
from puzzle.models import Puzzle
from .filters import WorkshopFilter, TagFilter, ORDER


class WorkshopView(TemplateView):
    template_name = 'puzzle/list.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'count': Puzzle.objects.get_queryset().filter(user__isnull=False, is_published=True).count(),
            'language': get_language(),
            'order': [(key, value['title']) for key, value in ORDER.items()],
        })
        return context


class WorkshopItems(ScrollListView):
    request: WSGILanguageRequest
    model = Puzzle

    def get_queryset(self) -> QuerySet[Puzzle]:
        qs = super().get_queryset().\
            filter(user__isnull=False, is_published=True,
                   translations__language_code=self.request.LANGUAGE_CODE).\
            prefetch_related('translations', 'user')
        return WorkshopFilter(self.request.GET, qs).qs.distinct()


class TagView(BaseListView):
    model = Tag

    def get_queryset(self) -> QuerySet[Tag]:
        return TagFilter(self.request.GET, super().get_queryset()).qs

    @staticmethod
    def convert_item(item: Tag) -> AutocompleteItem:
        return {'value': str(item.pk), 'label': item.name}

    def render_to_response(self, context, **kwargs) -> JsonResponse:
        return JsonResponse([self.convert_item(item) for item in context['object_list']], safe=False)

    def post(self, request, *args, **kwargs) -> Union[JsonResponse, HttpResponseBadRequest]:
        if not request.user.is_authenticated:
            return HttpResponseBadRequest(status=401)

        instance, _ = Tag.objects.get_or_create(name=request.POST['name'][:50])
        return JsonResponse(self.convert_item(instance))
