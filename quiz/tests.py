from django.test import TestCase
from django.urls import reverse

from quiz.factories import QuizFactory


class QuizTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(QuizTestCase, cls).setUpClass()
        cls.quiz = QuizFactory()

    def test_game(self):
        response = self.client.get(reverse('quiz_map', kwargs={'name': self.quiz.slug}))
        self.assertTemplateUsed(response, 'quiz/map.html')
