from django.apps import AppConfig
from django.db.models.signals import post_save


class PuzzleConfig(AppConfig):
    name = 'puzzle'

    def ready(self):
        from maps.signals import attach_translations

        post_save.connect(attach_translations, sender=self.models['puzzle'])
