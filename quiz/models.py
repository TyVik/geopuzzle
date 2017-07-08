from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from maps.models import Game, GameTranslation


QUIZ_OPTIONS = (
    ('name', 'name'),
    ('capital', 'capital'),
    ('flag', 'flag'),
    ('coat_of_arms', 'coat_of_arms')
)


class Quiz(Game):
    options = ArrayField(models.CharField(max_length=12, choices=QUIZ_OPTIONS),
                         default=['name', 'capital', 'flag', 'coat_of_arms'])

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def get_absolute_url(self) -> str:
        return reverse('quiz_map', args=(self.slug,))


class QuizTranslation(GameTranslation):
    master = models.ForeignKey(Quiz, related_name='translations', editable=False)

    class Meta:
        unique_together = ('language_code', 'master')
        db_table = 'quiz_quiz_translation'


@receiver(post_save, sender=Quiz)
def attach_translations(sender, instance, created, **kwargs):
    if created:
        common = {'master': instance, 'name': instance.slug}
        for lang, _ in settings.LANGUAGES:
            QuizTranslation.objects.create(language_code=lang, **common)
