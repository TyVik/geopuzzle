from django.contrib import admin

from maps.admin import GameAdmin
from puzzle.models import Puzzle


@admin.register(Puzzle)
class PuzzleAdmin(GameAdmin):
    pass
