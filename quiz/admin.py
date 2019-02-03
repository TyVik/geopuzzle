from django.contrib import admin
from django.contrib.admin import TabularInline

from maps.admin import GameAdmin
from quiz.models import Quiz, QuizTranslation, QuizRegion


class QuizTranslationInline(TabularInline):
    model = QuizTranslation
    extra = 0


class QuizRegionInline(TabularInline):
    model = QuizRegion
    extra = 0
    raw_id_fields = ('region',)
    autocomplete_lookup_fields = {
        'fk': ['region'],
    }


@admin.register(Quiz)
class QuizAdmin(GameAdmin):
    list_display = ('id', 'image_tag', 'names', 'slug', 'is_published', 'is_global', 'user')
    inlines = (QuizTranslationInline, QuizRegionInline)
    fieldsets = (
        (None, {
            'fields': (('slug', 'zoom', 'options'), ('is_published', 'is_global', 'on_main_page'),
                       ('image', 'user'), ('center',))
        }),
    )
    list_filter = ('is_published', 'on_main_page', 'user')
