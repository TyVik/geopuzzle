from typing import List

from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import success
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ImageField
from django.contrib.gis.db.models import MultiPolygonField, QuerySet
from django.contrib.gis.forms import OSMWidget
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from hvad.admin import TranslatableAdmin

from common.admin import ImageMixin, AdminImageWidget
from maps.forms import KMLCountryImportForm, KMLAreaImportForm
from maps.models import Country, Area


@admin.register(Country)
class CountryAdmin(ImageMixin, TranslatableAdmin):
    list_display = ('id', '_name', 'image_tag', 'slug', 'wikidata_id', 'is_published', 'is_global')
    list_display_links = ('image_tag', 'id', '_name')
    list_editable = ('wikidata_id',)
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
    }

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
                redirect_url = reverse('admin:{app}_{model}_changelist'.format(app=opts.app_label, model='country')) + '?meta__id__exact={}'.format(pk)
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


def recalc_answer(modeladmin, request, queryset) -> None:
    for area in queryset:
        area.recalc_answer()
    success(request, 'Answers were recalculated.')
recalc_answer.short_description = "Recalc answer"


def update_infobox(modeladmin, request, queryset) -> None:
    for area in queryset:
        area.update_infobox_by_instance()
    success(request, 'Infoboxes were updated.')
update_infobox.short_description = "Update infobox"


@admin.register(Area)
class AreaAdmin(TranslatableAdmin):
    list_display = ('_name', 'difficulty', 'wiki_id', 'num_points')
    list_filter = ('difficulty', 'country')
    list_editable = ('difficulty',)
    actions = [recalc_answer, update_infobox]
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
        MultiPolygonField: {'widget': OSMWidget},
    }

    def _name(self, obj: Area) -> str:
        return obj.name

    def num_points(self, obj: Area) -> int:
        return obj.polygon.num_points

    def wiki_id(self, obj: Area) -> str:
        infobox = obj.infobox
        if infobox is None:
            return ''
        instance = infobox.get('instance', None)
        return '' if instance is None else '<a href="{link}">{id}</a>'.format(link=instance, id=instance.split('/')[-1])
    wiki_id.short_description = 'Wiki ID'
    wiki_id.allow_tags = True

    def kml_import(self, request:WSGIRequest, pk: str) -> HttpResponse:
        opts = self.model._meta
        user = None
        if request.method == 'POST':
            form = KMLAreaImportForm(request.POST, request.FILES, initial={"area": pk})
            if form.is_valid():
                form.save()
                redirect_url = reverse('admin:{app}_{model}_change'.format(app=opts.app_label, model='area'), args=(pk,))
                success(request, 'KML "{}" was imported successfully.'.format(form.cleaned_data['kml']))
                return HttpResponseRedirect(redirect_url)
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
        ] + super(AreaAdmin, self).get_urls()
