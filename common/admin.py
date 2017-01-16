from django.conf import settings
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin.current import AdminImageWidget as SorlImageWidget


class AdminImageWidget(SorlImageWidget):
    def render(self, name, value, attrs=None):
        try:
            result = super(AdminImageWidget, self).render(name, value, attrs)
        except TypeError:  # base image does not exists
            result = 'Original image does not exists'
        return result


class ImageMixin(object):
    image_field = 'image'

    def image_tag(self, obj):
        return self.base_image_tag(obj)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    @classmethod
    def base_image_tag(cls, obj):
        image = getattr(obj, cls.image_field)
        url = settings.THUMBNAIL_DUMMY_SOURCE.format(width=80)
        try:
            thumb = get_thumbnail(image, 'x80', upscale=False, format='PNG')
            url = thumb.url
        except Exception as e:
            print(e)
        return '<img src="{}"/>'.format(url)
