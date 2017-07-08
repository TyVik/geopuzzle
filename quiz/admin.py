from django.contrib import admin
from django.contrib.admin import TabularInline

from maps.admin import GameAdmin
from quiz.models import Quiz, QuizTranslation


class QuizTranslationInline(TabularInline):
    model = QuizTranslation
    extra = 0


@admin.register(Quiz)
class QuizAdmin(GameAdmin):
    inlines = (QuizTranslationInline,)
