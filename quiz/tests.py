from typing import List

from django.test import TestCase
from django.urls import reverse

from .factories import QuizFactory, QuizRegionFactory
from .models import QuizRegion, Quiz


class QuizTestCase(TestCase):
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
        def get_ids(l):
            return [x['id'] for x in l]

        response = self.client.get(self._question_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['solved']), self.SOLVED_COUNT)
        self.assertEqual(len(data['questions']), self.QUESTIONS_COUNT)
        ids = get_ids(data['questions'])
        self.assertEqual(set(x.region.id for x in self.questions), set(ids))

        shuffled_retries = 4
        while shuffled_retries > 0:
            response = self.client.get(self._question_url)
            data = response.json()
            if ids != get_ids(data['questions']):
                break
            shuffled_retries -= 1
        else:
            self.failureException('Question random is broken')

    def test_custom_questions(self):
        response = self.client.get(f'{self._question_url}&id=1,2,3')
        self.assertEqual(response.status_code, 400)
        self.assertIn('id', response.json())

        response = self.client.get(f"{self._question_url}&id={self.questions[0].region_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['questions']), 1)
