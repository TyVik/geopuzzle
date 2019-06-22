from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string

from maps.models import Tag
from users.factories import UserFactory
from workshop.factories import TagFactory


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

        long_name = get_random_string(length=55)
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
        tag = TagFactory(name=get_random_string())

        response = self.client.get(self.url, {'name': tag.name[2:5]})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)

        unknown_name = get_random_string(length=20)
        response = self.client.get(self.url, {'name': unknown_name})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)
