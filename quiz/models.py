from typing import List

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext as _

from maps.models import Game, GameTranslation, Region

QUIZ_OPTIONS = (
    ('name', 'name'),
    ('capital', 'capital'),
    ('flag', 'flag'),
    ('coat_of_arms', 'coat_of_arms')
)


def default_quiz_options() -> List[str]:
    return [key for key, _ in QUIZ_OPTIONS]


class Quiz(Game):
    regions = models.ManyToManyField(Region, through='QuizRegion')
    options = ArrayField(models.CharField(max_length=12, choices=QUIZ_OPTIONS), default=default_quiz_options)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    @classmethod
    def name(cls) -> str:
        return _('Quiz')

    @classmethod
    def description(cls) -> str:
        return _('In the Quiz you need find the country by flag, emblem or the capital. Did you know that Monaco and Indonesia have the same flags? And that the flags of the United States and Liberia differ only in the number of stars? So, these and other interesting things can be learned and remembered after brainstorming right now!')


class QuizRegion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=False)


class QuizTranslation(GameTranslation):
    master = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='translations', editable=False)

    class Meta:
        unique_together = ('language_code', 'master')
        db_table = 'quiz_quiz_translation'
