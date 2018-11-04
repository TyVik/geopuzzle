from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import SafeText

from users.models import User


@admin.register(User)
class PuzzleAdmin(ModelAdmin):
    list_display = ('id', 'image_tag', 'username', 'is_active', 'language')
    list_display_links = ('image_tag', 'username')

    def image_tag(self, obj):
        return SafeText(f'<img src="{obj.image.name}"/>')
