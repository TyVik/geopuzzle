from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from common.utils import random_string
from maps.models import Tag
from puzzle.factories import PuzzleFactory
from users.factories import UserFactory
from .factories import TagFactory


class TagTestCase(TestCase):
    url = reverse('tag')

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_create(self):
        tag_name = 'New tag'
        response = self.client.post(self.url, {'name': tag_name})
        self.assertEqual(response.status_code, 401)

        self.client.force_login(self.user)
        response = self.client.post(self.url, {'name': tag_name})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        tag = Tag.objects.get(name=tag_name)
        self.assertEqual(data['value'], str(tag.id))
        self.assertEqual(data['label'], tag.name)

        long_name = random_string(length=55)
        response = self.client.post(self.url, {'name': long_name})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['label'], long_name[:50])

    def test_idempotency(self):
        tag = TagFactory()

        self.client.force_login(self.user)
        response = self.client.post(self.url, {'name': tag.name})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['value'], str(tag.id))
        self.assertEqual(data['label'], tag.name)

    def test_list(self):
        count = 5
        tags = [TagFactory() for _ in range(count)]

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), count)
        ids = [item['value'] for item in data]
        for tag in tags:
            self.assertIn(str(tag.id), ids)

    def test_filter(self):
        tag = TagFactory()

        response = self.client.get(self.url, {'name': tag.name[2:5]})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)

        unknown_name = random_string(length=20)
        response = self.client.get(self.url, {'name': unknown_name})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)


class WorkshopTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 1 global
        # 1 without user and published
        # 1 without user and not published
        # 1 with user and not published
        # 1 with user and published
        # 1 with user and published (for search)
        # 1 with user and published (for tag filter)
        # 1 with another user and published (for user filter)
        cls.user = UserFactory()
        cls.tag = TagFactory(name=random_string())
        cls.puzzles = {
            'global': PuzzleFactory(is_global=True),
            'without_user_and_published': PuzzleFactory(is_published=True, user=None),
            'without_user_and_not_published': PuzzleFactory(is_published=True, user=None),
            'not_published': PuzzleFactory(is_published=False, user=cls.user),
            'published': PuzzleFactory(is_published=True, user=cls.user),
            'published_search': PuzzleFactory(is_published=True, user=cls.user),
            'published_filter_tag': PuzzleFactory(is_published=True, user=cls.user),
            'published_filter_user': PuzzleFactory(is_published=True, user=UserFactory()),
        }
        cls.puzzles['published_filter_tag'].tags.add(cls.tag)

    def test_get(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'ru'})
        response = self.client.get(reverse('workshop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'puzzle/list.html')
        self.assertEqual(response.context_data['language'], 'ru')
        self.assertEqual(len(response.context_data['order']), 4)
        self.assertEqual(response.context_data['count'], 4)

    def _check_response(self, response, puzzle_keys):
        self.assertEqual(response.status_code, 200)
        db_names = [self.puzzles[key].load_translation('en').name for key in puzzle_keys]
        response_names = [item['name'] for item in response.json()]
        self.assertEqual(db_names, response_names)

    def test_list(self):
        response = self.client.get(reverse('workshop_items'))
        should_be = ('published_filter_user', 'published_filter_tag', 'published_search', 'published')
        self._check_response(response, should_be)

    def test_search(self):
        search_by = self.puzzles['published_search'].load_translation('en').name[:4]
        response = self.client.get(reverse('workshop_items'), {'search': search_by})
        should_be = ('published_search',)
        self._check_response(response, should_be)

    def test_filter_tag(self):
        response = self.client.get(reverse('workshop_items'), {'tag': self.tag.id})
        should_be = ('published_filter_tag',)
        self._check_response(response, should_be)

    def test_filter_user(self):
        response = self.client.get(reverse('workshop_items'), {'user': self.user.id})
        should_be = ('published_filter_tag', 'published_search', 'published')
        self._check_response(response, should_be)

    def test_order(self):
        available = ('published_filter_user', 'published_filter_tag', 'published_search', 'published')
        response = self.client.get(reverse('workshop_items'), {'order': 'title_asc'})
        temp = list({key: value.load_translation('en').name.lower() for key, value in self.puzzles.items() if key in available}.items())
        temp.sort(key=lambda x: x[1])
        should_be = [key[0] for key in temp]
        self._check_response(response, should_be)
