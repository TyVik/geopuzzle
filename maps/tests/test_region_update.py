from unittest import mock

from django.contrib.gis.geos import MultiPolygon
from django.test import TestCase as DjangoTestCase

from maps.forms import UpdateRegionForm
from maps.models import Region
from maps.factories import RegionFactory


class UpdateRegionTestCase(DjangoTestCase):
    region: Region

    @classmethod
    def setUpTestData(cls) -> None:
        cls.continent = RegionFactory(polygon=MultiPolygon(), osm_id=3)
        cls.country = RegionFactory(polygon=MultiPolygon(), osm_id=9407, parent=cls.continent, wikidata_id='Q228')
        cls.region = RegionFactory(polygon=MultiPolygon(), osm_id=2804753, parent=cls.country)

    @staticmethod
    def mocked_requests_head(*args, **kwargs):
        class MockResponse:
            def __init__(self, url, status_code):
                self.url = url
                self.status_code = status_code

        return MockResponse(args[0], 200)

    def test_update_region(self):
        # I won't use mocks in this case because update region is a critical flow.
        # I'd like to know as soon as possible if something will be broken here.
        form = UpdateRegionForm({'with_wiki': True, 'recursive': True, 'max_level': 12})
        form.is_valid()
        with mock.patch('requests.head', side_effect=self.mocked_requests_head):
            log = form.handle(self.region)
        self.assertIn('Q2522163', log)
        self.assertIn('Q1863', log)
        self.assertIn('Q24597', log)
        self.assertEqual(Region.objects.count(), 5)
