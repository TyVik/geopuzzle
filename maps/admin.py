from typing import Tuple, Union, Type

from admirarchy.utils import HierarchicalModelAdmin, AdjacencyList, HierarchicalChangeList, \
    Hierarchy
from django.contrib.admin import TabularInline
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.postgres.fields import JSONField
from django.template.defaultfilters import safe
from django.utils.safestring import SafeText
from django.utils.translation import ugettext as _

from django.contrib import admin
from django.db.models import ImageField
from django.contrib.gis.db.models import MultiPolygonField
from django.templatetags.static import static
from django_json_widget.widgets import JSONEditorWidget

from common.admin import ImageMixin, AdminImageWidget, MultiPolygonWidget, UserAutocompleteFilter
from common.utils import get_language
from .models import Region, RegionTranslation, Tag, Game


class RegionChangeList(HierarchicalChangeList):
    def get_queryset(self, request):
        return super().get_queryset(request).defer('polygon')

    def get_query_string(self, new_params=None, remove=None):
        remove = [] if remove is None else remove
        result = super().get_query_string(new_params, remove)
        if 'parent=None' not in result:
            result = result.replace(self.model_admin.hierarchy.pid_field,
                                    self.model_admin.hierarchy.PARENT_ID_QS_PARAM)
        return result


class RegionTranslationAdmin(admin.TabularInline):
    model = RegionTranslation
    extra = 0
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


class RegionAdjacencyList(AdjacencyList):
    def hook_get_queryset(self, changelist, request):
        super().hook_get_queryset(changelist, request)
        if (self.pid_field in changelist.params) and (changelist.params[self.pid_field] is None):
            del changelist.params[self.pid_field]


@admin.register(Region)
class RegionAdmin(HierarchicalModelAdmin):
    list_display = ('__str__', 'wikidata_url', 'osm_id', 'infobox_status')
    search_fields = ('wikidata_id__exact', 'translations__name')
    formfield_overrides = {
        MultiPolygonField: {'widget': MultiPolygonWidget},
        JSONField: {'widget': JSONEditorWidget},
    }
    hierarchy = RegionAdjacencyList('parent')
    inlines = (RegionTranslationAdmin,)
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': (('title', 'parent', 'is_enabled'),
                       ('osm_id', 'wikidata_id'),
                       '_osm_data',
                       'polygon')
        }),
    )

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    def get_changelist(self, request, **kwargs):
        Hierarchy.init_hierarchy(self)
        return RegionChangeList

    def wikidata_url(self, obj: Region) -> SafeText:
        link = obj._meta._forward_fields_map['wikidata_id'].link.format(id=obj.wikidata_id)  # pylint: disable=protected-access
        return safe(f'<a href="{link}" rel="noopener noreferrer">{obj.wikidata_id}</a>')

    def infobox_status(self, obj: Region) -> SafeText:
        result = ''
        if obj.pk is not None:
            for key, value in obj.infobox_status(get_language()).items():
                name = 'icon-{}.svg'.format('yes' if value else 'no')
                result += '<img src="{}" title="{}"/>'.format(static('admin/img/' + name), key)
        return safe(result)
    infobox_status.short_description = _('Infobox')
    infobox_status.allow_tags = True


class GameItemsInline(TabularInline):
    extra = 0
    raw_id_fields = ('region',)
    autocomplete_lookup_fields = {
        'fk': ['region'],
    }


class GameAdmin(ImageMixin, OSMGeoAdmin):
    search_fields = ('translations__name',)
    list_display: Tuple[str, ...] = \
        ('id', 'image_tag', 'names', 'slug', 'is_published', 'is_global', 'user')
    list_filter: Tuple[Union[str, Type[UserAutocompleteFilter]], ...] = \
        ('is_published', 'on_main_page', UserAutocompleteFilter)
    list_display_links = ('image_tag', 'id')
    autocomplete_fields = ('user',)
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
    }
    list_per_page = 20

    class Media:
        pass

    def names(self, obj: Game) -> SafeText:
        return safe("<br/>".join(f'{t.language_code}: {t.name}'
                                 for t in obj.translations.order_by('language_code').all()))


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
