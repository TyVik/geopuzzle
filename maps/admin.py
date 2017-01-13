import tempfile

from django.contrib.gis.gdal import DataSource

from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.gis.geos import MultiPolygon
from django.contrib.messages import success
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from maps.models import Meta, Map


class KMLImportForm(forms.Form):
    map = forms.ModelChoiceField(queryset=Meta.objects.all(), disabled=True)
    kml = forms.FileField()

    def save(self):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(self.cleaned_data['kml'].read())
            temp.seek(0)
            source = DataSource(temp.name)
            for layer in source:
                for feat in layer:
                    polygon = feat.geom.geos if isinstance(feat.geom.geos, MultiPolygon) else MultiPolygon(feat.geom.geos)
                    map = Map.objects.create(name=feat['Name'].value, meta=self.cleaned_data['map'], polygon=polygon)
                    map.recalc_answer()


@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    def kml_import(self, request, pk):
        opts = self.model._meta
        user = None
        if request.method == 'POST':
            form = KMLImportForm(request.POST, request.FILES, initial={'map': pk})
            if form.is_valid():
                form.save()
                redirect_url = reverse('admin:{app}_{model}_changelist'.format(app=opts.app_label, model='map')) + '?meta__id__exact={}'.format(pk)
                success(request, 'KML "{}" was imported successfully.'.format(form.cleaned_data['kml']))
                return HttpResponseRedirect(redirect_url)
        else:
            form = KMLImportForm(initial={'map': pk})

        context = dict(
            self.admin_site.each_context(request),
            title='KML Import',
            opts=opts,
            app_label=opts.app_label,
            form=form,
            user=user
        )
        return TemplateResponse(request, 'admin/maps/meta/map_kml_import.html', context)

    def get_urls(self):
        return [
            url(r'^(.+)/kml_import/$', staff_member_required(self.kml_import), name='map_kml_import'),
        ] + super(MetaAdmin, self).get_urls()


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'meta', 'difficulty')
    list_filter = ('difficulty', 'meta')
    list_editable = ('difficulty',)
    search_fields = ('name',)
    ordering = ('name',)
