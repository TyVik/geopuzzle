from django.utils.translation import ugettext as _
from django_filters import FilterSet, ModelChoiceFilter, OrderingFilter, CharFilter

from maps.models import Tag
from puzzle.models import Puzzle
from users.models import User

ORDER = {
    'title_asc': {'title': _('Title ↓'), 'query': 'translations__name'},
    'title_desc': {'title': _('Title ↑'), 'query': '-translations__name'},
    'created_asc': {'title': _('Created ↓'), 'query': 'created'},
    'created_desc': {'title': _('Created ↑'), 'query': '-created'}
}


class WorkshopFilter(FilterSet):
    search = CharFilter(field_name="translations__name", lookup_expr='icontains')
    user = ModelChoiceFilter(field_name="user", queryset=User.objects.all())
    tag = ModelChoiceFilter(field_name="tags__name", queryset=Tag.objects.all())
    order = OrderingFilter(fields=tuple((value['query'], key) for key, value in ORDER.items()))

    class Meta:
        model = Puzzle
        fields = ('user', 'tag', 'search')


class TagFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ('name',)
