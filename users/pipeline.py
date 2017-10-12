from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.vk import VKOAuth2


def user_details(strategy, response, backend, user=None, *args, **kwargs):
    if user:
        user.first_name = response.get('first_name')
        user.last_name = response.get('last_name')
        if isinstance(backend, FacebookOAuth2):
            value = response.get('locale', 'en_US')
            user.language = value.split('_')[0]
            value = response.get('picture', {'data': {'url': None}})
            user.image = value.get('data').get('url')
        elif isinstance(backend, VKOAuth2):
            user.language = 'ru'
            user.image = response.get('photo')

        strategy.storage.user.changed(user)
