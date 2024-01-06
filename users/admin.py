from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from social_django.models import UserSocialAuth

from common.admin import ImageMixin
from .models import User


class SocialAuthInlines(TabularInline):
    model = UserSocialAuth
    extra = 0


@admin.register(User)
class UserAdmin(ImageMixin, BaseUserAdmin):
    search_fields = ('username', 'email')
    list_filter = ('language', 'is_staff', 'is_subscribed')
    list_display = ('id', 'image_tag', 'username', 'is_active', 'language')
    list_display_links = ('image_tag', 'username')
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        ('General', {
            'fields': (
                ('username', 'password', 'email'),
                ('first_name', 'last_name'),
                ('image', 'language', 'is_subscribed')
            )
        }),
        ('Administrative', {
            'fields': (
                ('is_active', 'is_staff', 'is_superuser'),
                ('groups', 'user_permissions'),
                ('date_joined', 'last_login'),
            )
        })
    )

    inlines = (SocialAuthInlines,)
