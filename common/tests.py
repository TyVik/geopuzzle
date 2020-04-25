from typing import List

from common.utils import random_string


class TestFilterListMixin:
    def test_list(self):
        count = 5
        objs = [self.filter_list_factory() for _ in range(count)]

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), count)
        ids = [item['value'] for item in data]
        for obj in objs:
            self.assertIn(str(obj.pk), ids)

    def test_filter(self):
        obj = self.filter_list_factory()

        name = obj.name if hasattr(obj, 'name') else obj.username
        response = self.client.get(self.url, {'name': name[2:5]})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)

        unknown_name = random_string(length=20)
        response = self.client.get(self.url, {'name': unknown_name})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)


class TestGameMixin:
    @classmethod
    def _get_ids(cls, questions) -> List[int]:
        return [x['id'] for x in questions]

    def check_questions(self, url: str) -> List[int]:
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['solved']), self.SOLVED_COUNT)
        self.assertEqual(len(data['questions']), self.QUESTIONS_COUNT)
        ids = self._get_ids(data['questions'])
        self.assertEqual(set(x.region.pk for x in self.questions), set(ids))
        return ids

    def check_shuffle_questions(self, ids: List[int], url: str) -> None:
        shuffled_retries = 4
        while shuffled_retries > 0:
            response = self.client.get(url)
            data = response.json()
            if ids != self._get_ids(data['questions']):
                break
            shuffled_retries -= 1
        else:
            self.failureException('Question random is broken')
