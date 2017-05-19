from admirarchy.utils import HierarchicalModelAdmin, AdjacencyList, HierarchicalChangeList, Hierarchy
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
from maps.models import Region, RegionTranslation


def update_infoboxes(modeladmin, request, queryset) -> None:
    for area in queryset:
        area.update_infobox_by_wikidata_id()
    success(request, _('Infoboxes were updated.'))
update_infoboxes.short_description = _("Update infoboxes")


def update_polygons(modeladmin, request, queryset) -> None:
    for area in queryset:
        area.import_osm_polygon()
    success(request, _('Polygons were updated.'))
update_polygons.short_description = _("Update polygons")


class RegionChangeList(HierarchicalChangeList):

    def get_queryset(self, request):
        return super(RegionChangeList, self).get_queryset(request).defer('polygon')

    def get_query_string(self, new_params=None, remove=None):
        result = super(RegionChangeList, self).get_query_string(new_params, remove)
        result = result.replace(self.model_admin.hierarchy.pid_field, self.model_admin.hierarchy.PARENT_ID_QS_PARAM)
        return result


class RegionTranslationAdmin(admin.TabularInline):
    model = RegionTranslation
    extra = 0


@admin.register(Region)
class RegionAdmin(HierarchicalModelAdmin):
    list_display = ('title', 'wikidata_id', 'osm_id', 'infobox_status')
    actions = (update_infoboxes, update_polygons)
    formfield_overrides = {
        MultiPolygonField: {'widget': MultiPolygonWidget},
    }
    hierarchy = AdjacencyList('parent')
    inlines = (RegionTranslationAdmin,)
    list_per_page = 20

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    def get_changelist(self, request, **kwargs):
        Hierarchy.init_hierarchy(self)
        return RegionChangeList

    def infobox_status(self, obj: Region) -> str:
        result = ''
        for key, value in obj.infobox_status(get_language()).items():
            name = 'icon-{}.svg'.format('yes' if value else 'no')
            result += '<img src="{}" title="{}"/>'.format(static('admin/img/' + name), key)
        return result
    infobox_status.short_description = _('Infobox')
    infobox_status.allow_tags = True

    def osm_import(self, request: WSGIRequest, pk: str) -> HttpResponse:
        region = get_object_or_404(Region, pk=pk)
        region.import_osm_polygon()
        success(request, _('Polygon was imported successfully.'))
        url = reverse('admin:{app}_{model}_change'.format(app=self.model._meta.app_label, model='region'), args=(pk,))
        return HttpResponseRedirect(url)

    def get_urls(self) -> List:
        return [
            url(r'^(.+)/osm_import/$', staff_member_required(self.osm_import), name='area_osm_import'),
        ] + super(RegionAdmin, self).get_urls()


class GameAdmin(ImageMixin, admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'slug', 'is_published', 'is_global')
    list_display_links = ('image_tag', 'id')
    filter_horizontal = ('regions',)
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
    }
