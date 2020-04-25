from typing import List

from django.test import TestCase
from django.urls import reverse

from common.tests import TestGameMixin
from .factories import PuzzleFactory, PuzzleRegionFactory
from .models import Puzzle, PuzzleRegion


class PuzzleTestCase(TestGameMixin, TestCase):
    puzzle: Puzzle
    questions: List[PuzzleRegion]
    solved = List[PuzzleRegion]

    QUESTIONS_COUNT = 3
    SOLVED_COUNT = 1

    @classmethod
    def setUpClass(cls):
        super(PuzzleTestCase, cls).setUpClass()
        cls.puzzle = PuzzleFactory()
        cls.questions = [PuzzleRegionFactory(puzzle=cls.puzzle) for _ in range(cls.QUESTIONS_COUNT)]
        cls.solved = [PuzzleRegionFactory(puzzle=cls.puzzle, is_solved=True) for _ in range(cls.SOLVED_COUNT)]

    def test_game(self):
        response = self.client.get(reverse('puzzle_map', kwargs={'name': self.puzzle.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'puzzle/map.html')

    def test_questions(self):
        url = reverse('puzzle_questions', kwargs={'name': self.puzzle.slug})
        ids = self.check_questions(url)
        self.check_shuffle_questions(ids, reverse('puzzle_questions', kwargs={'name': self.puzzle.slug}))

    def test_custom_questions(self):
        url = reverse('puzzle_questions', kwargs={'name': self.puzzle.slug})
        response = self.client.get(f"{url}?id=1,2,3")
        self.assertEqual(response.status_code, 400)
        self.assertIn('id', response.json())

        response = self.client.get(f"{url}?id={self.questions[0].region_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['questions']), 1)
