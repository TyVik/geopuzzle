from django.conf import settings
from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

from common.utils import random_string
from .factories import UserFactory
from .models import User


class UserTestCase(TestCase):
    password: str
    user: User

    @classmethod
    def setUpTestData(cls):
        cls.password = random_string()
        cls.user = UserFactory()
        cls.user.set_password(cls.password)
        cls.user.save()

    def _is_authenticated(self) -> bool:
        user = auth.get_user(self.client)
        return user.is_authenticated

    def test_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

        password = random_string()
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(url, data={'username': self.user.username, 'password': password})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self._is_authenticated())

    def test_registration(self):
        username = random_string()
        password = random_string()
        credentials = {
            'username': username,
            'email': f'{username}@random.com',
            'password': password
        }
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'ru'})
        response = self.client.post(reverse('registration'), credentials)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self._is_authenticated())
        user = User.objects.get(username=username)
        self.assertEqual(user.language, 'ru')
        self.assertEqual(user.is_subscribed, True)

    def test_registration_duplicate_username(self):
        wrong = {
            'username': self.user.username,
            'email': f'{random_string()}@example.com',
            'password': random_string()
        }
        response = self.client.post(reverse('registration'), wrong)
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context_data['form'].errors)
        self.assertFalse(self._is_authenticated())

    def test_registration_duplicate_email(self):
        wrong = {
            'username': random_string(),
            'email': self.user.email,
            'password': random_string()
        }
        response = self.client.post(reverse('registration'), wrong)
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.context_data['form'].errors)
        self.assertFalse(self._is_authenticated())

    def test_profile(self):
        self.user.refresh_from_db()
        self.client.force_login(self.user, 'django.contrib.auth.backends.ModelBackend')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    def test_change_password(self):
        url = f"{reverse('profile')}?section=password"
        new_password = random_string()
        data = {
            'old_password': self.password,
            'new_password1': new_password,
            'new_password2': new_password,
        }
        self.user.refresh_from_db()
        self.client.force_login(self.user, 'django.contrib.auth.backends.ModelBackend')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.user.set_password(self.password)
        self.user.save()


class UserListTestCase(TestCase):
    url = reverse('users')

    def test_list(self):
        count = 5
        tags = [UserFactory() for _ in range(count)]

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), count)
        ids = [item['value'] for item in data]
        for tag in tags:
            self.assertIn(str(tag.id), ids)

    def test_filter(self):
        user = UserFactory()

        response = self.client.get(self.url, {'name': user.username[2:5]})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)

        unknown_name = random_string(length=20)
        response = self.client.get(self.url, {'name': unknown_name})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)
