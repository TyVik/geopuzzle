from django.conf import settings

from maps.models import Game


def attach_translations(sender, instance: Game, created, **kwargs):
    """This signal should be connected in apps.py each of game module."""

    if created:
        common = {'master': instance, 'name': instance.slug}
        for lang in settings.ALLOWED_LANGUAGES:
            instance.translations.model.objects.create(language_code=lang, **common)
