from admirarchy.utils import HierarchicalModelAdmin, AdjacencyList, HierarchicalChangeList, Hierarchy
from django.contrib.gis.admin import OSMGeoAdmin
from django.template.defaultfilters import safe
from django.utils.safestring import SafeText
from django.utils.translation import ugettext as _
from typing import List

from django.conf.urls import url
from django.utils.translation import get_language
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import success
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ImageField
from django.contrib.gis.db.models import MultiPolygonField
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.urls import reverse

from common.admin import ImageMixin, AdminImageWidget, MultiPolygonWidget
from .models import Region, RegionTranslation, Tag, Game


def update_infoboxes(modeladmin, request, queryset) -> None:
    for area in queryset:
        area.update_infobox()
    success(request, _('Infoboxes were updated.'))
update_infoboxes.short_description = _("Update infoboxes")


def update_polygons(modeladmin, request, queryset) -> None:
    for area in queryset:
        area.fetch_polygon()
    success(request, _('Polygons were updated.'))
update_polygons.short_description = _("Update polygons")


class RegionChangeList(HierarchicalChangeList):
    def get_queryset(self, request):
        return super(RegionChangeList, self).get_queryset(request).defer('polygon')

    def get_query_string(self, new_params=None, remove=None):
        remove = [] if remove is None else remove
        result = super(RegionChangeList, self).get_query_string(new_params, remove)
        if 'parent=None' not in result:
            result = result.replace(self.model_admin.hierarchy.pid_field, self.model_admin.hierarchy.PARENT_ID_QS_PARAM)
        return result


class RegionTranslationAdmin(admin.TabularInline):
    model = RegionTranslation
    extra = 0


class RegionAdjacencyList(AdjacencyList):
    def hook_get_queryset(self, changelist, request):
        super(RegionAdjacencyList, self).hook_get_queryset(changelist, request)
        if changelist.params[self.pid_field] is None:
            del changelist.params[self.pid_field]


@admin.register(Region)
class RegionAdmin(HierarchicalModelAdmin):
    list_display = ('__str__', 'wikidata_url', 'osm_id', 'infobox_status')
    search_fields = ('id', 'title', 'wikidata_id')
    actions = (update_infoboxes, update_polygons)
    formfield_overrides = {
        MultiPolygonField: {'widget': MultiPolygonWidget},
    }
    hierarchy = RegionAdjacencyList('parent')
    inlines = (RegionTranslationAdmin,)
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': (('title', 'parent', 'is_enabled'), ('osm_id', 'wikidata_id'), 'osm_data', 'polygon')
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
        link = obj._meta._forward_fields_map['wikidata_id'].link.format(id=obj.wikidata_id)
        return safe(f'<a href="{link}">{obj.wikidata_id}</a>')

    def infobox_status(self, obj: Region) -> SafeText:
        result = ''
        if obj.id is not None:
            for key, value in obj.infobox_status(get_language()).items():
                name = 'icon-{}.svg'.format('yes' if value else 'no')
                result += '<img src="{}" title="{}"/>'.format(static('admin/img/' + name), key)
        return safe(result)
    infobox_status.short_description = _('Infobox')
    infobox_status.allow_tags = True

    def infobox_import(self, request: WSGIRequest, pk: str) -> HttpResponse:
        region = get_object_or_404(Region, pk=pk)
        region.update_infobox()
        success(request, _('Infobox was updated successfully.'))
        url = reverse('admin:{app}_{model}_change'.format(app=self.model._meta.app_label, model='region'), args=(pk,))
        return HttpResponseRedirect(url)

    def osm_import(self, request: WSGIRequest, pk: str) -> HttpResponse:
        region = get_object_or_404(Region, pk=pk)
        region.fetch_polygon()
        success(request, _('Polygon was imported successfully.'))
        url = reverse('admin:{app}_{model}_change'.format(app=self.model._meta.app_label, model='region'), args=(pk,))
        return HttpResponseRedirect(url)

    def get_urls(self) -> List:
        return [
            url(r'^(.+)/infobox_import/$', staff_member_required(self.infobox_import), name='infobox_import'),
            url(r'^(.+)/osm_import/$', staff_member_required(self.osm_import), name='osm_import'),
        ] + super(RegionAdmin, self).get_urls()


class GameAdmin(ImageMixin, OSMGeoAdmin):
    list_display = ('id', 'image_tag', 'names', 'slug', 'is_published', 'is_global', 'user')
    list_display_links = ('image_tag', 'id')
    autocomplete_fields = ('regions',)
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
    }
    list_per_page = 20

    def names(self, obj: Game) -> SafeText:
        return safe("<br/>".join(f'{t.language_code}: {t.name}' for t in obj.translations.order_by('language_code').all()))


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
