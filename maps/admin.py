from django.utils.translation import ugettext as _
from typing import List

from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import success
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ImageField
from django.contrib.gis.db.models import MultiPolygonField, QuerySet, MultiPointField
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from hvad.admin import TranslatableAdmin

from common.admin import ImageMixin, AdminImageWidget, MultiPolygonWidget, MultiPointWidget
from maps.forms import KMLCountryImportForm, KMLAreaImportForm
from maps.models import Country, Area, Region


@admin.register(Country)
class CountryAdmin(ImageMixin, TranslatableAdmin):
    list_display = ('id', '_name', 'image_tag', 'slug', 'wikidata_id', 'is_published', 'is_global')
    list_display_links = ('image_tag', 'id', '_name')
    list_editable = ('wikidata_id',)
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
    }
    """
    fieldsets = (
        (None, {'fields': (
            ('wikidata_id', 'is_published', 'is_global', 'name'),
            ('image', 'slug', 'zoom'),
            'center', 'default_positions')}),
    )
    """

    def _name(self, obj: Country) -> str:
        return obj.name

    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        return super(CountryAdmin, self).get_queryset(request)

    def kml_import(self, request: WSGIRequest, pk: str) -> HttpResponse:
        opts = self.model._meta
        user = None
        if request.method == 'POST':
            form = KMLCountryImportForm(request.POST, request.FILES, initial={"country": pk})
            if form.is_valid():
                form.save()
                redirect_url = reverse('admin:{app}_{model}_changelist'.format(app=opts.app_label, model='country')) + \
                               '?meta__id__exact={}'.format(pk)
                success(request, 'KML "{}" was imported successfully.'.format(form.cleaned_data['kml']))
                return HttpResponseRedirect(redirect_url)
        else:
            form = KMLCountryImportForm(initial={"country": pk})

        context = dict(
            self.admin_site.each_context(request),
            title='KML Import',
            opts=opts,
            app_label=opts.app_label,
            form=form,
            user=user
        )
        return TemplateResponse(request, 'admin/maps/country/map_kml_import.html', context)

    def get_urls(self) -> List:
        return [
            url(r'^(.+)/kml_import/$', staff_member_required(self.kml_import), name='country_kml_import'),
        ] + super(CountryAdmin, self).get_urls()


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


@admin.register(Area)
class AreaAdmin(TranslatableAdmin):
    list_display = ('_name', 'difficulty', 'wikidata_id', 'osm_id', 'num_strip_points', 'num_points', 'infobox_status')
    list_filter = ('difficulty', 'country')
    list_editable = ('difficulty', 'wikidata_id', 'osm_id')
    actions = (update_infoboxes, update_polygons)
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
        MultiPolygonField: {'widget': MultiPolygonWidget},
        MultiPointField: {'widget': MultiPointWidget},
    }

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    def _name(self, obj: Area) -> str:
        return obj.name

    def num_points(self, obj: Area) -> int:
        return obj.polygon.num_points

    def num_strip_points(self, obj: Area) -> int:
        return obj.polygon.simplify(0.01).num_points

    def infobox_status(self, obj: Area) -> str:
        result = ''
        for key, value in obj.infobox_status().items():
            result += '<img src="/static/admin/img/icon-{}.svg" title="{}"/>'.format('yes' if value else 'no', key)
        return result
    infobox_status.short_description = _('Infobox')
    infobox_status.allow_tags = True

    def formchange_url(self, pk: str) -> str:
        return reverse('admin:{app}_{model}_change'.format(app=self.model._meta.app_label, model='area'), args=(pk,))

    def osm_import(self, request: WSGIRequest, pk: str) -> HttpResponse:
        area = get_object_or_404(Area, pk=pk)
        area.import_osm_polygon()
        success(request, _('Polygon was imported successfully.'))
        return HttpResponseRedirect(self.formchange_url(pk))

    def kml_import(self, request:WSGIRequest, pk: str) -> HttpResponse:
        opts = self.model._meta
        user = None
        if request.method == 'POST':
            form = KMLAreaImportForm(request.POST, request.FILES, initial={"area": pk})
            if form.is_valid():
                form.save()
                success(request, 'KML "{}" was imported successfully.'.format(form.cleaned_data['kml']))
                return HttpResponseRedirect(self.formchange_url(pk))
        else:
            form = KMLAreaImportForm(initial={"area": pk})

        context = dict(
            self.admin_site.each_context(request),
            title='KML Import',
            opts=opts,
            app_label=opts.app_label,
            form=form,
            user=user
        )
        return TemplateResponse(request, 'admin/maps/area/map_kml_import.html', context)

    def get_urls(self) -> List:
        return [
            url(r'^(.+)/kml_import/$', staff_member_required(self.kml_import), name='area_kml_import'),
            url(r'^(.+)/osm_import/$', staff_member_required(self.osm_import), name='area_osm_import'),
        ] + super(AreaAdmin, self).get_urls()


@admin.register(Region)
class RegionAdmin(TranslatableAdmin):
    list_display = ('title', 'wikidata_id', 'osm_id')
    list_editable = ('wikidata_id', 'osm_id')
    actions = (update_infoboxes, update_polygons)
    formfield_overrides = {
        MultiPolygonField: {'widget': MultiPolygonWidget},
    }

    class Media:
        css = {
            'all': ('css/admin.css',)
        }
