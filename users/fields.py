import os
from io import BytesIO

from PIL import Image
from awesome_avatar.fields import AvatarField
from awesome_avatar.settings import config
from django.core.files.uploadedfile import InMemoryUploadedFile


class CustomAvatarField(AvatarField):
    def save_form_data(self, instance, data):
        # if data and self.width and self.height:
        file_ = None
        if hasattr(data, '__getitem__'):
            file_ = data['file']
        if file_:

            image = Image.open(file_)
            image = image.crop(data['box'])
            if not getattr(config, 'no_resize', False):
                image = image.resize((self.width, self.height), Image.ANTIALIAS)

            content = BytesIO()
            image.save(content, config.save_format, quality=config.save_quality)

            file_name = u'{}.{}'.format(os.path.splitext(file_.name)[0], config.save_format)

            # new_data = SimpleUploadedFile(file.name, content.getvalue(), content_type='image/' + config.save_format)
            new_data = InMemoryUploadedFile(content, None, file_name, 'image/' + config.save_format, len(content.getvalue()), None)
            super(AvatarField, self).save_form_data(instance, new_data)
