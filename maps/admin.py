from django.contrib import admin

from maps.models import Meta, World


@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    pass


@admin.register(World)
class World(admin.ModelAdmin):
    pass