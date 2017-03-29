from django.contrib import admin

from quiz.models import Option


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    filter_horizontal = ('countries',)