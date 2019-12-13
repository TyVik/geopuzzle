import os
from io import FileIO
from urllib.request import urlretrieve

from django.conf import settings
from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.vk import VKOAuth2

from .models import User


def user_details(strategy, response, backend, is_new, user=None, *args, **kwargs):
    def save_image(user: User, url: str):
        if url:
            result = urlretrieve(url)
            user.image.save(os.path.basename(url), FileIO(result[0]))
            user.save()

    if user is not None and is_new:
        fields = {'first_name': None, 'last_name': None, 'language': None, 'image_url': None}

        if isinstance(backend, FacebookOAuth2):
            locale = response.get('locale', 'en_US')
            image = response.get('picture', {'data': {'url': None}})
            fields.update({
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name'),
                'language': locale.split('_')[0],
                'image_url': image.get('data').get('url'),
            })
        elif isinstance(backend, VKOAuth2):
            fields.update({
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name'),
                'language': 'ru',
                'image_url': response.get('photo'),
            })
        elif isinstance(backend, GoogleOAuth2):
            fields.update({
                'first_name': response.get('given_name'),
                'last_name': response.get('family_name'),
                'language': response['locale'],
                'image_url': response['picture'],
            })

        user.first_name = fields['first_name']
        user.last_name = fields['last_name']
        user.language = fields['language'] if fields['language'] in settings.ALLOWED_LANGUAGES else 'en'
        strategy.storage.user.changed(user)
        save_image(user, fields['image_url'])
