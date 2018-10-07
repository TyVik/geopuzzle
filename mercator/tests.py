from django.test import TestCase
from django.urls import reverse

from puzzle.factories import PuzzleFactory
from quiz.factories import QuizFactory


class StaticViewsTestCase(TestCase):
    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'robots.txt')

    def test_sitemap_xml(self):
        puzzle = PuzzleFactory()
        quiz = QuizFactory()
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(f'http://testserver{puzzle.get_absolute_url()}', response.rendered_content)
        self.assertInHTML(f'http://testserver{quiz.get_absolute_url()}', response.rendered_content)
        self.assertInHTML(f'http://testserver{reverse("index")}', response.rendered_content)

    def test_error(self):
        response = self.client.get(reverse('error'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('Something went wrong :(', response.content.decode())
