from django.contrib import admin
from django.contrib.admin import TabularInline

from maps.admin import GameAdmin
from puzzle.models import Puzzle, PuzzleTranslation, PuzzleRegion


class PuzzleTranslationInline(TabularInline):
    model = PuzzleTranslation
    extra = 0


class PuzzleRegionInline(TabularInline):
    model = PuzzleRegion
    extra = 0
    raw_id_fields = ('region',)
    autocomplete_lookup_fields = {
        'fk': ['region'],
    }


@admin.register(Puzzle)
class PuzzleAdmin(GameAdmin):
    inlines = (PuzzleTranslationInline, PuzzleRegionInline)
    fieldsets = (
        (None, {
            'fields': (('slug', 'zoom', 'is_published', 'is_global'), ('image', 'user'),
                       ('center', 'default_positions'))
        }),
    )
    list_filter = ('user', 'is_published')
