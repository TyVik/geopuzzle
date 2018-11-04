from django.contrib import admin
from django.contrib.admin import ModelAdmin

from common.admin import ImageMixin
from users.models import User


@admin.register(User)
class UserAdmin(ImageMixin, ModelAdmin):
    list_display = ('id', 'image_tag', 'username', 'is_active', 'language')
    list_display_links = ('image_tag', 'username')
