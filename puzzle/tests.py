from django.test import TestCase
from django.urls import reverse

from puzzle.factories import PuzzleFactory


class PuzzleTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PuzzleTestCase, cls).setUpClass()
        cls.puzzle = PuzzleFactory()

    def test_game(self):
        response = self.client.get(reverse('puzzle_map', kwargs={'name': self.puzzle.slug}))
        self.assertTemplateUsed(response, 'puzzle/map.html')
