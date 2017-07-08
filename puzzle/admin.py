from django.contrib import admin
from django.contrib.admin import TabularInline

from maps.admin import GameAdmin
from puzzle.models import Puzzle, PuzzleTranslation


class PuzzleTranslationInline(TabularInline):
    model = PuzzleTranslation
    extra = 0


@admin.register(Puzzle)
class PuzzleAdmin(GameAdmin):
    inlines = (PuzzleTranslationInline,)
