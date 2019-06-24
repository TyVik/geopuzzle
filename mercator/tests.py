from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from puzzle.factories import PuzzleFactory
from quiz.factories import QuizFactory


class StaticViewsTestCase(TestCase):
    def setUp(self) -> None:
        cache.delete_pattern('views.decorators.cache.cache_page*')

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'robots.txt')

        cached = self.client.get('/robots.txt')
        self.assertEqual(cached.status_code, 200)
        self.assertEqual(cached.templates, [])
        self.assertEqual(cached.content, response.content)

    def test_sitemap_xml(self):
        puzzle = PuzzleFactory()
        quiz = QuizFactory()
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(f'http://testserver{puzzle.get_absolute_url()}', response.rendered_content)
        self.assertInHTML(f'http://testserver{quiz.get_absolute_url()}', response.rendered_content)
        self.assertInHTML(f'http://testserver{reverse("index")}', response.rendered_content)

        cached = self.client.get('/sitemap.xml')
        self.assertEqual(cached.status_code, 200)
        self.assertEqual(cached.content, response.content)

    def test_error(self):
        response = self.client.get(reverse('error'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('Something went wrong :(', response.content.decode())

    def test_status(self):
        response = self.client.get(reverse('status'))
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['redis'], 'success')
        self.assertEqual(content['database'], 'success')
