from django.contrib import admin
from django.contrib.admin import TabularInline
from django.template.defaultfilters import safe

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
    list_display = ('id', 'image_tag', 'slug', 'is_published', 'is_global', 'user', 'tag_list')
    inlines = (PuzzleTranslationInline, PuzzleRegionInline)
    fieldsets = (
        (None, {
            'fields': (('slug', 'zoom', 'is_published', 'is_global'), ('image', 'user'),
                       ('center', 'default_positions'), 'tags')
        }),
    )
    filter_horizontal = ('tags',)
    list_filter = ('user', 'is_published')

    def tag_list(self, obj: Puzzle) -> str:
        return safe(', '.join(x.name_en for x in obj.tags.all()))
