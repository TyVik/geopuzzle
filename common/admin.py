from admin_auto_filters.filters import AutocompleteFilter
from django.conf import settings
from django.template.defaultfilters import safe
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin.current import AdminImageWidget as SorlImageWidget


class AdminImageWidget(SorlImageWidget):
    def render(self, name, value, attrs=None, **kwargs) -> str:
        try:
            result = super().render(name, value, attrs, **kwargs)
        except TypeError:
            result = 'Original image does not exists'
        return result


class ImageMixin:
    image_field = 'image'

    def image_tag(self, obj) -> str:
        return self.base_image_tag(obj)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    @classmethod
    def base_image_tag(cls, obj) -> str:
        image = getattr(obj, cls.image_field)
        url = settings.THUMBNAIL_DUMMY_SOURCE.replace('%(width)s', '80')
        try:
            thumb = get_thumbnail(image, 'x80', upscale=False, format='PNG')
            url = thumb.url
        except Exception as exception:  # pylint: disable=broad-except
            print(exception)
        return safe('<img src="{}"/>'.format(url))


class UserAutocompleteFilter(AutocompleteFilter):
    title = 'user'
    field_name = 'user'
