from django.contrib import admin

from maps.admin import GameAdmin
from quiz.models import Option, Quiz


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    filter_horizontal = ('countries',)


@admin.register(Quiz)
class QuizAdmin(GameAdmin):
    pass
