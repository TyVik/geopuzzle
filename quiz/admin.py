from django.contrib import admin
from django.contrib.admin import TabularInline

from maps.admin import GameAdmin, GameItemsInline
from .models import Quiz, QuizTranslation, QuizRegion


class QuizTranslationInline(TabularInline):
    model = QuizTranslation
    extra = 0


class QuizRegionInline(GameItemsInline):
    model = QuizRegion


@admin.register(Quiz)
class QuizAdmin(GameAdmin):
    inlines = (QuizTranslationInline, QuizRegionInline)
    fieldsets = (
        (None, {
            'fields': (('slug', 'zoom', 'options'), ('is_published', 'is_global', 'on_main_page'),
                       ('image', 'user'), ('center',))
        }),
    )
