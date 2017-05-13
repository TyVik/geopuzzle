from admirarchy.utils import HierarchicalModelAdmin, AdjacencyList, HierarchicalChangeList, Hierarchy
from django.contrib.gis.forms import BaseGeometryWidget
from django.utils.translation import ugettext as _
from typing import List

from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import success
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ImageField
from django.contrib.gis import gdal
from django.contrib.gis.db.models import MultiPolygonField
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from floppyforms.gis.widgets import MultiPolygonWidget
from hvad.admin import TranslatableAdmin

from common.admin import ImageMixin, AdminImageWidget
from maps.models import Region, RegionTranslationProxy


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


class OSMSecureWidget(BaseGeometryWidget):
    """
    An OpenLayers/OpenStreetMap-based widget.
    """
    template_name = 'gis/openlayers-osm.html'
    default_lon = 5
    default_lat = 47

    class Media:
        js = (
            'https://openlayers.org/api/2.13.1/OpenLayers.js',
            'gis/js/OLMapWidget.js',
        )

    def __init__(self, attrs=None):
        super(OSMSecureWidget, self).__init__()
        for key in ('default_lon', 'default_lat'):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)

    @property
    def map_srid(self):
        # Use the official spherical mercator projection SRID when GDAL is
        # available; otherwise, fallback to 900913.
        if gdal.HAS_GDAL:
            return 3857
        else:
            return 900913


class RegionTranslationProxyAdmin(admin.TabularInline):
    model = RegionTranslationProxy
    extra = 0


@admin.register(Region)
class RegionAdmin(HierarchicalModelAdmin):
    list_display = ('title', 'wikidata_id', 'osm_id')
    actions = (update_infoboxes, update_polygons)
    formfield_overrides = {
        # MultiPolygonField: {'widget': OSMSecureWidget},
        MultiPolygonField: {'widget': MultiPolygonWidget},
    }
    hierarchy = AdjacencyList('parent')
    inlines = (RegionTranslationProxyAdmin,)
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
        for key, value in obj.infobox_status().items():
            result += '<img src="/static/admin/img/icon-{}.svg" title="{}"/>'.format('yes' if value else 'no', key)
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


class GameAdmin(ImageMixin, TranslatableAdmin):
    list_display = ('id', 'image_tag', 'slug', 'is_published', 'is_global')
    list_display_links = ('image_tag', 'id')
    filter_horizontal = ('regions',)
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
    }
