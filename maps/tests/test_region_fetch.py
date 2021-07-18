from copy import deepcopy

from django.test import TestCase as DjangoTestCase
from django.urls import reverse

from maps.models import Region
from maps.factories import RegionFactory, INFOBOX, multipolygon_factory


class RegionTestCase(DjangoTestCase):
    region: Region

    @classmethod
    def setUpTestData(cls):
        cls.region = RegionFactory(polygon=multipolygon_factory())

    def test_full_info(self):
        infobox = deepcopy(INFOBOX)
        del infobox['geonamesID']
        del infobox['capital']['id']
        infobox['marker'] = {'lat': 12.516, 'lng': -70.033}

        response = self.client.get(reverse('region', args=(self.region.pk,)))
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['id'], self.region.pk)
        self.assertEqual(len(content['polygon']), 2)  # 2 islands
        self.assertDictEqual(content['infobox'], infobox)
