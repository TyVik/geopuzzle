import os
from io import FileIO
from urllib.request import urlretrieve

from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.vk import VKOAuth2


def user_details(strategy, response, backend, is_new, user=None, *args, **kwargs):
    if user is not None and is_new:
        image_url = None
        user.first_name = response.get('first_name')
        user.last_name = response.get('last_name')
        if isinstance(backend, FacebookOAuth2):
            value = response.get('locale', 'en_US')
            user.language = value.split('_')[0]
            value = response.get('picture', {'data': {'url': None}})
            image_url = value.get('data').get('url')
        elif isinstance(backend, VKOAuth2):
            user.language = 'ru'
            image_url = response.get('photo')
        elif isinstance(backend, GoogleOAuth2):
            user.language = response['language']
            value = response.get('image', {'url': None})
            image_url = value.get('url')
            user.first_name = response['name'].get('givenName')
            user.last_name = response['name'].get('familyName')

        strategy.storage.user.changed(user)
        if image_url:
            result = urlretrieve(image_url)
            user.image.save(os.path.basename(image_url), FileIO(result[0]))
            user.save()
