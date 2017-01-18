from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages import success
from django.contrib.postgres.fields import JSONField
from django.db.models import ImageField
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from jsoneditor.forms import JSONEditor

from common.admin import ImageMixin, AdminImageWidget
from maps.forms import KMLImportForm
from maps.models import Country, Area


@admin.register(Country)
class CountryAdmin(ImageMixin, admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'name', 'slug')
    list_display_links = ('image_tag', 'name', 'id',)
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
        JSONField: {'widget': JSONEditor},
    }
    fieldsets = (
        (None, {'fields':
                    (('name', 'slug'), 'image', ('zoom', 'default_count'), 'center', 'position', 'sparql')
                }),
    )

    def kml_import(self, request, pk):
        opts = self.model._meta
        user = None
        if request.method == 'POST':
            form = KMLImportForm(request.POST, request.FILES, initial={"country": pk})
            if form.is_valid():
                form.save()
                redirect_url = reverse('admin:{app}_{model}_changelist'.format(app=opts.app_label, model='country')) + '?meta__id__exact={}'.format(pk)
                success(request, 'KML "{}" was imported successfully.'.format(form.cleaned_data['kml']))
                return HttpResponseRedirect(redirect_url)
        else:
            form = KMLImportForm(initial={"country": pk})

        context = dict(
            self.admin_site.each_context(request),
            title='KML Import',
            opts=opts,
            app_label=opts.app_label,
            form=form,
            user=user
        )
        return TemplateResponse(request, 'admin/maps/country/map_kml_import.html', context)

    def get_urls(self):
        return [
            url(r'^(.+)/kml_import/$', staff_member_required(self.kml_import), name='map_kml_import'),
        ] + super(CountryAdmin, self).get_urls()


def recalc_answer(modeladmin, request, queryset):
    for area in queryset:
        area.recalc_answer()
    success(request, 'Answers were recalculated.')
recalc_answer.short_description = "Recalc answer"


def update_infobox(modeladmin, request, queryset):
    for area in queryset:
        area.update_infobox()
    success(request, 'Infoboxes were updated.')
update_infobox.short_description = "Update infobox"


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'difficulty')
    list_filter = ('difficulty', 'country')
    list_editable = ('difficulty',)
    search_fields = ('name',)
    actions = [recalc_answer, update_infobox]
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget},
        JSONField: {'widget': JSONEditor},
    }
