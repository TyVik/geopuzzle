from django.contrib import admin

from maps.models import Meta, World


@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    pass


@admin.register(World)
class World(admin.ModelAdmin):
    list_display = ('name', 'difficulty')
    list_filter = ('difficulty',)
    list_editable = ('difficulty',)
    search_fields = ('name',)
    ordering = ('name',)