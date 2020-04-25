from django.apps import AppConfig
from django.db.models.signals import post_save


class QuizConfig(AppConfig):
    name = 'quiz'

    def ready(self):
        from maps.signals import attach_translations  # pylint: disable=import-outside-toplevel

        post_save.connect(attach_translations, sender=self.models['quiz'])
