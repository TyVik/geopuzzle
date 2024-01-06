from io import BytesIO
from typing import Optional
from urllib.parse import unquote, urlparse

import requests
from django.conf import settings
from django.utils.crypto import get_random_string
from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.vk import VKOAuth2

from .models import User


def user_details(strategy, response, backend, is_new, *args, user=None, **kwargs):
    def save_image(user: User, url: Optional[str]) -> None:
        if url:
            result = requests.get(unquote(url), timeout=2.0)
            ext = urlparse(url).path.split('.')[-1]
            user.image.save(f'{get_random_string(16)}.{ext}', BytesIO(result.content))
            user.save()

    if user is not None and is_new:
        fields = {'first_name': '', 'last_name': '', 'language': None, 'image_url': None}

        if isinstance(backend, FacebookOAuth2):
            locale = response.get('locale', 'en_US')
            image = response.get('picture', {'data': {'url': None}})
            fields.update({
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', ''),
                'language': locale.split('_')[0],
                'image_url': image.get('data').get('url'),
            })
        elif isinstance(backend, VKOAuth2):
            fields.update({
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', ''),
                'language': 'ru',
                'image_url': response.get('photo'),
            })
        elif isinstance(backend, GoogleOAuth2):
            fields.update({
                'first_name': response.get('given_name', ''),
                'last_name': response.get('family_name', ''),
                'language': response['locale'],
                'image_url': response['picture'],
            })

        user.first_name = fields['first_name']
        user.last_name = fields['last_name']
        user.language = fields['language'] if fields['language'] in settings.ALLOWED_LANGUAGES else 'en'
        strategy.storage.user.changed(user)
        save_image(user, fields['image_url'])
