from django.contrib import admin

from maps.admin import GameAdmin
from quiz.models import Quiz


@admin.register(Quiz)
class QuizAdmin(GameAdmin):
    pass
