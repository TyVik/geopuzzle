from django.contrib import admin
from django.contrib.admin import TabularInline
from django.template.defaultfilters import safe

from common.admin import UserAutocompleteFilter
from maps.admin import GameAdmin, GameItemsInline
from .models import Puzzle, PuzzleTranslation, PuzzleRegion


class PuzzleTranslationInline(TabularInline):
    model = PuzzleTranslation
    extra = 0


class PuzzleRegionInline(GameItemsInline):
    model = PuzzleRegion


@admin.register(Puzzle)
class PuzzleAdmin(GameAdmin):
    list_display = ('id', 'image_tag', 'names', 'slug', 'is_published', 'is_global', 'user', 'tag_list')
    inlines = (PuzzleTranslationInline, PuzzleRegionInline)
    fieldsets = (
        (None, {
            'fields': (('slug', 'zoom'), ('is_published', 'is_global', 'on_main_page'), ('image', 'user'),
                       ('center', 'default_positions'), 'tags')
        }),
    )
    filter_horizontal = ('tags',)
    list_filter = ('is_published', 'on_main_page', UserAutocompleteFilter, 'tags')

    class Media:
        pass

    def tag_list(self, obj: Puzzle) -> str:
        return safe(', '.join(x.name for x in obj.tags.all()))
