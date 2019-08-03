from django.apps import AppConfig
from django.db.models.signals import post_save


class QuizConfig(AppConfig):
    name = 'quiz'

    def ready(self):
        from maps.models import Game
        from maps.signals import attach_translations

        for model in self.models:
            if isinstance(model, Game):
                post_save.connect(attach_translations, sender=model)
