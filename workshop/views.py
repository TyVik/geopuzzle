from django.views.generic import TemplateView
from django.utils.translation import get_language

from common.views import ScrollListView
from maps.models import Tag
from puzzle.models import Puzzle


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


class WorkshopItems(ScrollListView):
    model = Puzzle

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
