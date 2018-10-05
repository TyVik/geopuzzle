from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string

from users.factories import UserFactory


class UserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(UserTestCase, cls).setUpClass()
        cls.user = UserFactory()

    def test_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

        password = get_random_string()
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(url, data={'username': self.user.username, 'password': password})
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
