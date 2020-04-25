from typing import List

from django.test import TestCase
from django.urls import reverse

from common.tests import TestGameMixin
from .factories import QuizFactory, QuizRegionFactory
from .models import QuizRegion, Quiz


class QuizTestCase(TestGameMixin, TestCase):
    quiz: Quiz
    questions: List[QuizRegion]
    solved = List[QuizRegion]

    QUESTIONS_COUNT = 3
    SOLVED_COUNT = 1

    @classmethod
    def setUpClass(cls):
        super(QuizTestCase, cls).setUpClass()
        cls.quiz = QuizFactory()
        cls.questions = [QuizRegionFactory(quiz=cls.quiz) for _ in range(cls.QUESTIONS_COUNT)]
        cls.solved = [QuizRegionFactory(quiz=cls.quiz, is_solved=True) for _ in range(cls.SOLVED_COUNT)]

    def test_game(self):
        response = self.client.get(reverse('quiz_map', kwargs={'name': self.quiz.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/map.html')

    @property
    def _question_url(self) -> str:
        return f"{reverse('quiz_questions', kwargs={'name': self.quiz.slug})}?params=title,capital"

    def test_questions(self):
        ids = self.check_questions(self._question_url)
        self.check_shuffle_questions(ids, self._question_url)

    def test_custom_questions(self):
        response = self.client.get(f'{self._question_url}&id=1,2,3')
        self.assertEqual(response.status_code, 400)
        self.assertIn('id', response.json())

        response = self.client.get(f"{self._question_url}&id={self.questions[0].region_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['questions']), 1)
